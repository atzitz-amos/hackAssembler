from SymbolTable import SymbolTable
from Tokenizer import Token


class CompileEngine:
    def __init__(self, tokenizer, vmwriter):
        self.tokenizer = tokenizer

        self.class_name = None
        self.label_counter = -1

        self.symbol_table = SymbolTable()
        self.vmwriter = vmwriter

    def increment_label(self):
        self.label_counter += 1
        return f".L{self.label_counter}"

    def eat(self, token_type):
        s = self.tokenizer.advance()
        if s.type != token_type:
            raise Exception(
                f'Expected {["KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"][token_type]}, got {["KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"][s.type]}')
        return s

    def consume_keyword(self, *names):
        x = self.eat(Token.KEYWORD)
        assert x.value in names, f"Expected one of {names}, got {x.value}"
        return x

    def consume_symbol(self, *symbols):
        x = self.eat(Token.SYMBOL)
        assert x.value in symbols, f"Expected one of {symbols}, got {x.value}"
        return x

    def compile_class(self):
        self.consume_keyword("class")
        self.class_name = self.eat(Token.IDENTIFIER).value
        self.consume_symbol("{")

        while self.tokenizer.seek().value != "}":
            if self.tokenizer.seek().value == "static" or self.tokenizer.seek().value == "field":
                self.compile_class_var_dec()
            elif self.tokenizer.seek().value in ["constructor", "function", "method"]:
                self.compile_subroutine()

        self.consume_symbol("}")

    def compile_class_var_dec(self):
        kind = self.consume_keyword("field", "static").value
        if self.tokenizer.seek().value in ["int", "char", "boolean"]:
            type_ = self.consume_keyword("int", "char", "boolean").value
        else:
            type_ = self.eat(Token.IDENTIFIER).value

        name = self.eat(Token.IDENTIFIER).value
        self.symbol_table.define(name, type_, kind)

        while self.tokenizer.seek().value == ",":
            self.consume_symbol(",")
            name = self.eat(Token.IDENTIFIER).value
            self.symbol_table.define(name, type_, kind)

        self.consume_symbol(";")

    def compile_subroutine(self):
        self.symbol_table.start_subroutine()

        kind = self.consume_keyword("constructor", "function", "method").value
        if self.tokenizer.seek().value in ["void", "int", "char", "boolean"]:
            rettype = self.consume_keyword("void", "int", "char", "boolean").value
        else:
            rettype = self.eat(Token.IDENTIFIER).value

        if kind == "method":
            self.symbol_table.define("this", self.class_name, "argument")

        name = self.eat(Token.IDENTIFIER).value
        self.consume_symbol("(")
        self.compile_parameter_list()
        self.consume_symbol(")")

        self.compile_subroutine_decl()
        self.vmwriter.write_function(f"{self.class_name}.{name}", self.symbol_table.get_count("local"))
        if kind == "constructor":
            self.vmwriter.write_push("constant", self.symbol_table.get_count("field"))
            self.vmwriter.write_call("Memory.alloc", 1)
            self.vmwriter.write_pop("pointer", 0)
        elif kind == "method":
            self.vmwriter.write_push("argument", 0)
            self.vmwriter.write_pop("pointer", 0)

        self.compile_subroutine_body()

    def compile_parameter_list(self):
        if self.tokenizer.seek().value == ")":
            return
        if self.tokenizer.seek().value in ["int", "char", "boolean"]:
            type_ = self.consume_keyword("int", "char", "boolean").value
        else:
            type_ = self.eat(Token.IDENTIFIER).value
        name = self.eat(Token.IDENTIFIER).value
        self.symbol_table.define(name, type_, "argument")

        while self.tokenizer.seek().value == ",":
            self.consume_symbol(",")
            if self.tokenizer.seek().value in ["int", "char", "boolean"]:
                type_ = self.consume_keyword("int", "char", "boolean").value
            else:
                type_ = self.eat(Token.IDENTIFIER).value
            self.symbol_table.define(self.eat(Token.IDENTIFIER).value, type_, "argument")

    def compile_subroutine_body(self):
        self.compile_statements()
        self.consume_symbol("}")

    def compile_subroutine_decl(self):
        self.consume_symbol("{")
        while self.tokenizer.seek().value == "var":
            self.compile_var_dec()

    def compile_var_dec(self):
        self.consume_keyword("var")
        if self.tokenizer.seek().value in ["int", "char", "boolean"]:
            type_ = self.consume_keyword("int", "char", "boolean").value
        else:
            type_ = self.eat(Token.IDENTIFIER).value
        self.symbol_table.define(self.eat(Token.IDENTIFIER).value, type_, "local")

        while self.tokenizer.seek().value == ",":
            self.consume_symbol(",")
            self.symbol_table.define(self.eat(Token.IDENTIFIER).value, type_, "local")

        self.consume_symbol(";")

    def compile_statements(self):
        while self.tokenizer.seek().value != "}":
            if self.tokenizer.seek().value == "let":
                self.compile_let()
            elif self.tokenizer.seek().value == "if":
                self.compile_if()
            elif self.tokenizer.seek().value == "while":
                self.compile_while()
            elif self.tokenizer.seek().value == "do":
                self.compile_do()
            elif self.tokenizer.seek().value == "return":
                self.compile_return()

    def compile_let(self):
        self.consume_keyword("let")
        varname = self.eat(Token.IDENTIFIER).value
        if self.tokenizer.seek().value == "[":
            return self.compile_array_set(varname)
        self.consume_symbol("=")
        self.compile_expression()
        kind = self.symbol_table.get_kind(varname)
        if kind == "field":
            kind = "this"
        self.vmwriter.write_pop(kind, self.symbol_table.get_index(varname))
        self.consume_symbol(";")

    def compile_array_set(self, varname):
        self.consume_symbol("[")

        self.compile_expression()
        self.vmwriter.write_push(self.symbol_table.get_kind(varname), self.symbol_table.get_index(varname))

        self.vmwriter.write_arithmetic("add")

        self.consume_symbol("]")
        self.consume_symbol("=")

        self.compile_expression()
        self.vmwriter.write_pop("temp", 0)
        self.vmwriter.write_pop("pointer", 1)
        self.vmwriter.write_push("temp", 0)
        self.vmwriter.write_pop("that", 0)

        self.consume_symbol(";")

    def compile_if(self):
        self.consume_keyword("if")
        self.consume_symbol("(")

        self.compile_expression()
        self.vmwriter.write_arithmetic("not")

        label = self.increment_label()
        self.vmwriter.write_if(label)

        self.consume_symbol(")")
        self.consume_symbol("{")
        self.compile_statements()
        self.consume_symbol("}")
        if self.tokenizer.seek().value == "else":
            label2 = self.increment_label()
            self.vmwriter.write_goto(label2)
            self.vmwriter.write_label(label)

            self.consume_keyword("else")
            self.consume_symbol("{")
            self.compile_statements()
            self.consume_symbol("}")
            self.vmwriter.write_label(label2)
        else:
            self.vmwriter.write_label(label)

    def compile_while(self):
        label = self.increment_label()
        label_exit = self.increment_label()
        self.vmwriter.write_label(label)

        self.consume_keyword("while")
        self.consume_symbol("(")

        self.compile_expression()
        self.vmwriter.write_arithmetic("not")
        self.vmwriter.write_if(label_exit)

        self.consume_symbol(")")
        self.consume_symbol("{")
        self.compile_statements()
        self.vmwriter.write_goto(label)
        self.consume_symbol("}")

        self.vmwriter.write_label(label_exit)

    def compile_do(self):
        self.consume_keyword("do")
        self.compile_subroutine_call(self.eat(Token.IDENTIFIER).value)
        self.vmwriter.write_pop("temp", 0)
        self.consume_symbol(";")

    def compile_subroutine_call(self, name):
        this_param = 0
        if self.tokenizer.seek().value == ".":
            self.consume_symbol(".")
            type_ = self.symbol_table.get_type(name)
            kind = self.symbol_table.get_kind(name)
            if kind == "field":
                kind = "this"
            if kind is not None:
                this_param = 1
                self.vmwriter.write_push(kind, self.symbol_table.get_index(name))
            name = type_ + "." + self.eat(Token.IDENTIFIER).value
        else:
            self.vmwriter.write_push("pointer", 0)
            this_param = 1
            name = f"{self.class_name}.{name}"
        self.consume_symbol("(")
        length = self.compile_expression_list()
        self.vmwriter.write_call(name, length + this_param)
        self.consume_symbol(")")

    def compile_return(self):
        self.consume_keyword("return")
        if self.tokenizer.seek().value != ";":
            self.compile_expression()
        else:
            self.vmwriter.write_push("constant", 0)
        self.vmwriter.write_return()
        self.consume_symbol(";")

    def compile_expression(self):
        self.compile_term()
        while self.tokenizer.seek().value in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            symbol = self.consume_symbol("+", "-", "*", "/", "&", "|", "<", ">", "=").value
            self.compile_term()

            if symbol == "+":
                self.vmwriter.write_arithmetic("add")
            elif symbol == "-":
                self.vmwriter.write_arithmetic("sub")
            elif symbol == "*":
                self.vmwriter.write_call("Math.multiply", 2)
            elif symbol == "/":
                self.vmwriter.write_call("Math.divide", 2)
            elif symbol == "&":
                self.vmwriter.write_arithmetic("and")
            elif symbol == "|":
                self.vmwriter.write_arithmetic("or")
            elif symbol == "<":
                self.vmwriter.write_arithmetic("lt")
            elif symbol == ">":
                self.vmwriter.write_arithmetic("gt")
            elif symbol == "=":
                self.vmwriter.write_arithmetic("eq")

    def parse_string_const(self):
        string = self.eat(Token.STRING_CONST).value
        self.vmwriter.write_push("constant", len(string))
        self.vmwriter.write_call("String.new", 1)
        for char in string:
            self.vmwriter.write_push("constant", ord(char))
            self.vmwriter.write_call("String.appendChar", 2)

    def parse_keyword_const(self):
        keyword = self.eat(Token.KEYWORD).value
        if keyword == "true":
            self.vmwriter.write_push("constant", 0)
            self.vmwriter.write_arithmetic("not")
        elif keyword == "false":
            self.vmwriter.write_push("constant", 0)
        elif keyword == "null":
            self.vmwriter.write_push("constant", 0)
        elif keyword == "this":
            self.vmwriter.write_push("pointer", 0)

    def compile_term(self):
        if self.tokenizer.seek().type == Token.INT_CONST:
            self.vmwriter.write_push("constant", self.eat(Token.INT_CONST).value)
        elif self.tokenizer.seek().type == Token.STRING_CONST:
            self.parse_string_const()
        elif self.tokenizer.seek().value in ["true", "false", "null", "this"]:
            self.parse_keyword_const()
        elif self.tokenizer.seek().value == "(":
            self.consume_symbol("(")
            self.compile_expression()
            self.consume_symbol(")")
        elif self.tokenizer.seek().value in ["-", "~"]:
            sym = self.consume_symbol("-", "~").value
            self.compile_term()
            if sym == "-":
                self.vmwriter.write_arithmetic("neg")
            else:
                self.vmwriter.write_arithmetic("not")
        else:
            identifier = self.eat(Token.IDENTIFIER).value
            if self.tokenizer.seek().value == "[":
                self.consume_symbol("[")
                self.compile_expression()
                self.vmwriter.write_push(self.symbol_table.get_kind(identifier),
                                         self.symbol_table.get_index(identifier))
                self.vmwriter.write_arithmetic("add")
                self.vmwriter.write_pop("pointer", 1)
                self.vmwriter.write_push("that", 0)
                self.consume_symbol("]")
            elif self.tokenizer.seek().value in ["(", "."]:
                self.compile_subroutine_call(identifier)
            else:
                kind = self.symbol_table.get_kind(identifier)
                if kind == "field":
                    kind = "this"

                self.vmwriter.write_push(kind,
                                         self.symbol_table.get_index(identifier))

    def compile_expression_list(self):
        length = 0
        if self.tokenizer.seek().value != ")":
            self.compile_expression()
            length += 1
            while self.tokenizer.seek().value == ",":
                self.consume_symbol(",")
                self.compile_expression()
                length += 1
        return length
