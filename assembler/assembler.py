import time


def displayHelp():
    print(
        "Usage: "
        "assembler.py <filename> [<target>]"
    )


class CompileError(ValueError):
    def __init__(self, line, message):
        pass


class Parser:

    def __init__(self, cont):
        self.cont = cont

        self.symbols = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "SCREEN": 16384,
            "KBD": 24576
        }
        self.symbols.update({("R" + str(i)): i for i in range(16)})

        self.variable_counter = 0

        self.instructions = []

        self.currentline = 0
        self.currentline_noblank = 0

    def source(self, line):
        if line == "":
            return
        i = -1
        while i < len(line) - 1:
            i += 1
            char = line[i]
            if char == " " or char == "\t":
                continue
            elif char == "/" and i < len(line) - 2 and line[i + 1] == "/":
                break
            yield char

    def makeA(self, value):
        value = bin(value)[2:]
        if len(value) > 15:
            raise CompileError(self.currentline, "Invalid value for A instruction")
        value = "0" * (15 - len(value)) + value
        return "0" + value

    def makeC(self, dest, comput, jump):
        comput_table = {
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "!D": "0001101",
            "!A": "0110001",
            "-D": "0001111",
            "-A": "0110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "D+A": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "D|A": "0010101",

            "M": "1110000",
            "!M": "1110001",
            "-M": "1110011",
            "M+1": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "D-M": "1010011",
            "M-D": "1000111",
            "D&M": "1000000",
            "D|M": "1010101"
        }
        jump_table = {
            None: "000",
            "JGT": "001",
            "JEQ": "010",
            "JLT": "100",
            "JNE": "101",
            "JGE": "011",
            "JLE": "110",
            "JMP": "111"
        }

        if comput not in comput_table:
            raise CompileError(self.currentline, "Unknown computation: " + comput)
        comput_bytes = comput_table[comput]

        if jump not in jump_table:
            raise CompileError(self.currentline, "Unknown jump instruction: " + jump)
        jump_bytes = jump_table[jump]

        if dest:
            aregbit = "1" if "A" in dest else "0"
            dregbit = "1" if "D" in dest else "0"
            mregbit = "1" if "M" in dest else "0"
        else:
            aregbit = "0"
            dregbit = "0"
            mregbit = "0"

        return "111" + comput_bytes + aregbit + dregbit + mregbit + jump_bytes

    def parseA(self, source):
        value = "".join(source)
        if value.isnumeric():
            self.instructions.append(self.makeA(int(value)))
        elif value in self.symbols:
            self.instructions.append(self.makeA(self.symbols[value]))
        else:
            self.instructions.append((value,))

    def parseParen(self, source):
        if not source.endswith(")"):
            raise CompileError(self.currentline, "Expected closing parenthesis")
        self.symbols[source[:-1]] = self.currentline_noblank
        self.currentline_noblank -= 1

    def parseC(self, source):
        if "=" in source:
            destination, right = source.split("=")
        else:
            destination = None
            right = source
        if ";" in right:
            computation, jump = right.split(";")
        else:
            computation = right
            jump = None

        self.instructions.append(self.makeC(destination, computation, jump))

    def parse(self):
        for line in self.cont:
            try:
                source = self.source(line)

                begin = next(source)
                if begin == "@":
                    self.parseA(source)
                elif begin == "(":
                    self.parseParen("".join(source))
                else:
                    self.parseC(begin + "".join(source))
                self.currentline_noblank += 1
                self.currentline += 1
            except StopIteration:
                self.currentline += 1

        result = ""
        for i, instruction in enumerate(self.instructions):
            if type(instruction) is tuple:
                if instruction[0] not in self.symbols:
                    self.symbols[instruction[0]] = self.variable_counter + 16
                    self.variable_counter += 1
                instruction = self.makeA(self.symbols[instruction[0]])

            result += instruction + "\n"

        return result


def compileASM(cont: list) -> str:
    return Parser(cont).parse()


if __name__ == '__main__':
    import sys
    import os

    filename = sys.argv[1]

    if filename == "/?":
        displayHelp()
        sys.exit(0)

    filename = filename if filename.endswith('.asm') else filename + ".asm"
    if len(sys.argv) >= 3:
        targetfile = sys.argv[2]
        targetfile = targetfile if targetfile.endswith('.hack') else targetfile + ".hack"
    else:
        targetfile = filename[:-4] + ".hack"

    print(f"Loading {filename}...")

    with open(filename, 'r') as ioreader:
        content = ioreader.read().split("\n")

    print(f"Assembling {filename}...")

    t = time.time()
    compiled = compileASM(content)

    print(f"Successfully assembled {filename} in {time.time() - t} seconds")

    with open(targetfile, 'w') as iowriter:
        iowriter.write(compiled)

    os.system("pause")
