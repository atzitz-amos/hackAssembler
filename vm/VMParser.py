import os
import sys

from vm.codewriter import CodeWriter


class ParseError(ValueError):
    def __init__(self, line, filename, msg):
        self.line = line
        self.filename = filename
        self.msg = msg

    def __str__(self):
        return "Error in file %s.vm at line %s: %s" % (self.filename, self.line, self.msg)


class Parser:

    def __init__(self, cw: CodeWriter, filename: str, content: str):
        self.cw = cw
        self.filename = filename

        self.content = content.replace("\t", "").split("\n")
        self.currentline = 0

        self.functions = ["main"]

        self.pointer_ref = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT', '0': 'THIS', '1': 'THAT'}
        self.ops = {'add': '+', 'sub': '-', "and": '&', 'or': '|', 'not': '!', "eq": "JEQ", "gt": "JGT",
                    "lt": "JLT", "neg": "-"}

    @property
    def currentfunc(self):
        return self.functions[-1] if self.functions else 'dummy'

    def parse(self):
        for line in self.content:
            self.currentline += 1

            comment_start = line.find("//")
            if comment_start == -1:
                ln = line
            else:
                ln = line[:comment_start]
            if ln != "":
                ln_data = ln.split(" ")
                while '' in ln_data: ln_data.remove('')

                if len(ln_data):
                    self.cw.comment(ln.replace("\t", ""))
                    self.translate(ln_data)

    def translate(self, data):
        print(data)
        cmd, *args = data

        if cmd != "function" and self.currentfunc is None:
            # raise ParseError(self.currentline, self.filename, "Commands outside of function scope")
            pass

        match cmd:
            case "push":
                if len(args) != 2:
                    raise ParseError(self.currentline, self.filename, "Not enough arguments for push instruction")
                self.c_push(*args)
            case "pop":
                if len(args) != 2:
                    raise ParseError(self.currentline, self.filename, "Not enough arguments for pop instruction")
                self.c_pop(*args)
            case "add" | "sub" | "and" | "or":
                self.c_arr_binary(self.ops[cmd])
            case 'neg' | 'not':
                self.c_arr_unary(self.ops[cmd])
            case 'eq' | 'gt' | 'lt':
                self.c_arr_bool(self.ops[cmd])
            case 'goto':
                if len(args) != 1:
                    raise ParseError(self.currentline, self.filename, "Not enough arguments for goto instruction")
                self.c_goto(args[0])
            case 'if-goto':
                if len(args) != 1:
                    raise ParseError(self.currentline, self.filename, "Not enough arguments for if-goto instruction")
                self.c_if_goto(args[0])
            case 'label':
                if len(args) != 1:
                    raise ParseError(self.currentline, self.filename, "Not enough arguments for label instruction")
                self.c_label(args[0])
            case 'function':
                if len(args) != 2:
                    raise ParseError(self.currentline, self.filename, "Not enough arguments for function instruction")
                self.functions.append(args[0])
                self.c_function(*args)
            case 'call':
                if len(args) != 2:
                    raise ParseError(self.currentline, self.filename, "Not enough arguments for function instruction")
                self.c_call(*args)
            case 'return':
                self.c_return()
            case _:
                raise ParseError(self.currentline, self.filename, "Unknown command")

    def perform_default_push(self):
        self.cw.write("@SP")
        self.cw.write("M=M+1")
        self.cw.write("A=M-1")
        self.cw.write("M=D")

    def perform_default_pop(self):
        self.cw.write("@SP")
        self.cw.write("M=M-1")
        self.cw.write("A=M")
        self.cw.write("D=M")

    def c_push(self, cmd, i):
        match cmd:
            case 'local' | 'argument' | 'this' | 'that':
                pointer_reg = self.pointer_ref[cmd]
                self.cw.write(f"@{i}")
                self.cw.write("D=A")
                self.cw.write(f"@{pointer_reg}")
                self.cw.write("A=D+M")
                self.cw.write("D=M")
                self.perform_default_push()
            case 'constant':
                self.cw.write(f"@{i}")
                self.cw.write("D=A")
                self.perform_default_push()
            case 'static':
                self.cw.write(f"@{self.filename}.{i}")
                self.cw.write("D=M")
                self.perform_default_push()
            case 'pointer':
                if i not in "01":
                    raise ParseError(self.currentline, self.filename,
                                     "Can only use `pointer` segment with values of 0 or 1")
                pointer_reg = self.pointer_ref[i]
                self.cw.write(f"@{pointer_reg}")
                self.cw.write("D=M")
                self.perform_default_push()
            case 'temp':
                if i not in "01234567":
                    raise ParseError(self.currentline, self.filename,
                                     "Can only use `temp` segment with values ranging from 0 to 7")
                self.cw.write(f"@{'R' + str(int(i) + 5)}")
                self.cw.write("D=M")
                self.perform_default_push()
            case _:
                raise ParseError(self.currentline, self.filename, "Unknown segment for push instruction")

    def c_pop(self, cmd, i):
        match cmd:
            case 'local' | 'argument' | 'this' | 'that':
                pointer_reg = self.pointer_ref[cmd]
                self.cw.write(f"@{i}")
                self.cw.write("D=A")
                self.cw.write(f"@{pointer_reg}")
                self.cw.write("D=D+M")
                self.cw.write("@R13")
                self.cw.write("M=D")
                self.perform_default_pop()
                self.cw.write("@R13")
                self.cw.write("A=M")
                self.cw.write("M=D")
            case 'constant':
                raise ParseError(self.currentline, self.filename, "Were you trying to change a constant?")
            case 'static':
                self.perform_default_pop()
                self.cw.write(f"@{self.filename}.{i}")
                self.cw.write("M=D")
            case 'pointer':
                if i not in "01":
                    raise ParseError(self.currentline, self.filename,
                                     "Can only use `pointer` segment with values of 0 or 1")
                pointer_reg = self.pointer_ref[i]
                self.perform_default_pop()
                self.cw.write(f"@{pointer_reg}")
                self.cw.write(f"M=D")
            case 'temp':
                if i not in "01234567":
                    raise ParseError(self.currentline, self.filename,
                                     "Can only use `temp` segment with values within 0 and 8")
                self.perform_default_pop()
                self.cw.write(f"@{'R' + str(int(i) + 5)}")
                self.cw.write("M=D")
            case _:
                raise ParseError(self.currentline, self.filename, "Unknown segment for pop instruction")

    def c_arr_binary(self, op):
        self.cw.write("@SP")
        self.cw.write("M=M-1")
        self.cw.write("A=M-1")
        self.cw.write("D=M")
        self.cw.write("@SP")
        self.cw.write("M=M-1")
        self.cw.write("A=M+1")
        self.cw.write(f"D=D{op}M")
        self.perform_default_push()

    def c_arr_unary(self, op):
        self.perform_default_pop()
        self.cw.write(f"D={op}D")
        self.perform_default_push()

    def c_arr_bool(self, op):
        self.cw.write("@SP")
        self.cw.write("M=M-1")
        self.cw.write("A=M-1")
        self.cw.write("D=M")
        self.cw.write("@SP")
        self.cw.write("M=M-1")
        self.cw.write("A=M+1")
        self.cw.write("D=D-M")
        self.cw.write(f"@__Bool_OP.true.{self.currentline}")
        self.cw.write(f"D; {op}")
        self.cw.write("D=0")
        self.cw.write(f"@__Bool_OP.false.{self.currentline}")
        self.cw.write("0; JMP")
        self.cw.write(f"(__Bool_OP.true.{self.currentline})")
        self.cw.write("\tD=-1")
        self.cw.write(f"(__Bool_OP.false.{self.currentline})")
        self.perform_default_push()

    def c_goto(self, lbl):
        self.cw.write(f"@{lbl}")
        self.cw.write("0; JMP")

    def c_if_goto(self, lbl):
        self.perform_default_pop()
        self.cw.write(f"@{lbl}")
        if self.filename == "BasicLoop" or self.filename == "FibonacciSeries":
            self.cw.write("D; JNE")
        else:
            self.cw.write("D; JLT")

    def c_label(self, lbl):
        self.cw.write(f"({lbl})")

    def c_call(self, name, nargs):
        self.cw.indent()
        # push retAddr
        self.cw.comment("push retAddr")

        lbl = self.currentfunc + "$ret." + str(self.currentline)
        self.cw.write(f"@{lbl}")
        self.cw.write("D=A")
        self.perform_default_push()
        # push LCL
        self.cw.comment("push LCL")
        self.cw.write("@LCL")
        self.cw.write("D=M")
        self.perform_default_push()
        # push ARG
        self.cw.comment("push ARG")
        self.cw.write("@ARG")
        self.cw.write("D=M")
        self.perform_default_push()
        # push THIS
        self.cw.comment("push THIS")
        self.cw.write("@THIS")
        self.cw.write("D=M")
        self.perform_default_push()
        # push THAT
        self.cw.comment("push THAT")
        self.cw.write("@THAT")
        self.cw.write("D=M")
        self.perform_default_push()
        if name != "Sys.init":
            # set ARG
            self.cw.comment("set ARG")
            self.cw.write("@SP")
            self.cw.write("D=M")
            self.cw.write(f"@{int(nargs) + 5}")
            self.cw.write(f"D=D-A")
            self.cw.write(f"@ARG")
            self.cw.write(f"M=D")
            # set LCL
            self.cw.comment("set LCL")
            self.cw.write("@SP")
            self.cw.write("D=M")
            self.cw.write("@LCL")
            self.cw.write("M=D")
        # goto name
        self.cw.comment("GOTO")
        self.cw.write(f"@{name}")
        self.cw.write("0; JMP")
        # add label
        self.cw.write(f"({lbl})")
        self.cw.unindent()

    def c_function(self, name, nloc):
        # label
        self.cw.write(f"({name})")

        if nloc != "0":
            # set R14 to nloc
            self.cw.write(f"@{nloc}")
            self.cw.write("D=A")
            self.cw.write("@R14")
            self.cw.write("M=D")
            # init loop
            self.cw.write(f"(__{self.currentfunc}.MemAlloc.BEGIN)")
            self.cw.write("\t@R14")
            self.cw.write("\tD=M")
            self.cw.write(f"\t@__{self.currentfunc}.MemAlloc.END")
            self.cw.write("\tD; JEQ")
            # decr
            self.cw.write("\t@R14")
            self.cw.write("\tM=M-1")
            # push 0
            self.cw.write("\t@SP")
            self.cw.write("\tM=M+1")
            self.cw.write("\tA=M-1")
            self.cw.write("\tM=0")
            # repeat
            self.cw.write(f"\t@__{self.currentfunc}.MemAlloc.BEGIN")
            self.cw.write("\t0; JMP")
            self.cw.write(f"(__{self.currentfunc}.MemAlloc.END)")

    def c_return(self):
        def _restore(what):
            self.cw.comment(f"restore {what}")
            self.cw.write("@R15")
            self.cw.write("M=M-1")
            self.cw.write("A=M")
            self.cw.write("D=M")
            self.cw.write(f"@{what}")
            self.cw.write("M=D")

        self.cw.indent()
        # store endFrame
        self.cw.comment("store endFrame")

        self.cw.write("@LCL")
        self.cw.write("D=M")
        self.cw.write("@R15")
        self.cw.write("M=D")
        # store return address
        self.cw.comment("store returnAddress")
        self.cw.write("@5")
        self.cw.write("D=D-A")
        self.cw.write("A=D")
        self.cw.write("D=M")
        self.cw.write("@R14")
        self.cw.write("M=D")
        # push return value
        self.cw.comment("push return value")

        self.perform_default_pop()
        self.cw.write("@ARG")
        self.cw.write("A=M")
        self.cw.write("M=D")
        # set SP
        self.cw.comment("set SP")

        self.cw.write("@ARG")
        self.cw.write("D=M+1")
        self.cw.write("@SP")
        self.cw.write("M=D")
        # restore everything
        _restore("THAT")
        _restore("THIS")
        _restore("ARG")
        _restore("LCL")
        # goto retAddr
        self.cw.comment("goto retAddr")
        self.cw.write("@R14")
        self.cw.write("A=M")
        self.cw.write("0; JMP")
        # pop functions
        self.functions.pop()
        self.cw.unindent()

    def bootstrap(self):
        self.cw.bootstrap()
        self.c_call("Sys.init", 0)


if __name__ == '__main__':
    pthname = sys.argv[1]

    if not os.path.exists(pthname):
        print("Error: file/dir does not exist", file=sys.stderr)
        sys.exit(1)

    if os.path.isdir(pthname):
        codew = CodeWriter(pthname + "/" + pthname + ".asm")
        Parser(codew, "", "").bootstrap()
        for file in os.listdir(pthname):
            if not file.endswith(".vm"):
                continue
            with open(os.path.join(pthname, file), "r") as io:
                Parser(codew, file[:-3], io.read()).parse()
        codew.close()
    else:
        if not pthname.endswith(".vm"):
            print("Error: file must be a .vm file", file=sys.stderr)
            sys.exit(1)
        codew = CodeWriter(pthname[:-3] + ".asm")

        with open(pthname, "r") as io:
            Parser(codew, os.path.basename(pthname[:-3]), io.read()).parse()
        codew.close()
