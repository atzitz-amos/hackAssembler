import re
from xml.etree import cElementTree as ET

from Tokenizer import Token


class XMLWriter:

    def __init__(self, root):
        self.current = root
        self.stack = []

    def subnode(self, key):
        self.stack.append(self.current)
        self.current = ET.SubElement(self.current, key)
        return self

    def write(self, key, value):
        ET.SubElement(self.current, key).text = value

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.current = self.stack.pop()


class CompileEngine:
    def __init__(self, tokenizer, stream):
        self.tokenizer = tokenizer
        self.stream = stream

        print(self.tokenizer.seek())
        self.root = None
        self.xml_writer = None

    def eat(self, token_type):
        s = self.tokenizer.advance()
        if s.type != token_type:
            raise Exception(
                f'Expected {["KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"][token_type]}, got {["KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"][s.type]}')
        return s

    def parse_class(self):
        self.root = ET.Element("class")
        self.xml_writer = XMLWriter(self.root)

        self.consume_keyword("class")
        self.consume_identifier()
        self.consume_symbol("{")

        while self.tokenizer.seek().value != "}":
            if self.tokenizer.seek().value == "static" or self.tokenizer.seek().value == "field":
                self.parse_class_var_dec()
            elif self.tokenizer.seek().value in ["constructor", "function", "method"]:
                self.parse_subroutine()

        self.consume_symbol("}")

    def consume_keyword(self, *names):
        x = self.eat(Token.KEYWORD)
        assert x.value in names, f"Expected one of {names}, got {x.value}"
        self.xml_writer.write("keyword", x.value)

    def consume_symbol(self, *symbols):
        x = self.eat(Token.SYMBOL)
        assert x.value in symbols, f"Expected one of {symbols}, got {x.value}"
        self.xml_writer.write("symbol", x.value)

    def consume_int_const(self):
        self.xml_writer.write("integerConstant", self.eat(Token.INT_CONST).value)

    def consume_string_const(self):
        self.xml_writer.write("stringConstant", self.eat(Token.STRING_CONST).value)

    def consume_keyword_constant(self):
        x = self.eat(Token.KEYWORD)
        assert x.value in ["true", "false", "null", "this"]
        self.xml_writer.write("keyword", x.value)

    def consume_identifier(self):
        self.xml_writer.write("identifier", self.eat(Token.IDENTIFIER).value)

    def parse_class_var_dec(self):
        with self.xml_writer.subnode("classVarDec"):
            self.consume_keyword("field", "static")
            if self.tokenizer.seek().value in ["int", "char", "boolean"]:
                self.consume_keyword("int", "char", "boolean")
            else:
                self.consume_identifier()

            self.consume_identifier()

            while self.tokenizer.seek().value == ",":
                self.consume_symbol(",")
                self.consume_identifier()

            self.consume_symbol(";")

    def parse_subroutine(self):
        with self.xml_writer.subnode("subroutineDec"):
            self.consume_keyword("constructor", "function", "method")
            if self.tokenizer.seek().value == "void":
                self.consume_keyword("void")
            else:
                self.consume_identifier()
            self.consume_identifier()
            self.consume_symbol("(")
            self.parse_parameter_list()
            self.consume_symbol(")")
            self.parse_subroutine_body()

    def parse_parameter_list(self):
        with self.xml_writer.subnode("parameterList"):
            if self.tokenizer.seek().value == ")":
                return
            if self.tokenizer.seek().value in ["int", "char", "boolean"]:
                self.consume_keyword("int", "char", "boolean")
            else:
                self.consume_identifier()
            self.consume_identifier()

            while self.tokenizer.seek().value == ",":
                self.consume_symbol(",")
                if self.tokenizer.seek().value in ["int", "char", "boolean"]:
                    self.consume_keyword("int", "char", "boolean")
                else:
                    self.consume_identifier()
                self.consume_identifier()

    def parse_subroutine_body(self):
        with self.xml_writer.subnode("subroutineBody"):
            self.consume_symbol("{")
            while self.tokenizer.seek().value == "var":
                self.parse_var_dec()
            self.parse_statements()
            self.consume_symbol("}")

    def parse_var_dec(self):
        with self.xml_writer.subnode("varDec"):
            self.consume_keyword("var")
            if self.tokenizer.seek().value in ["int", "char", "boolean"]:
                self.consume_keyword("int", "char", "boolean")
            else:
                self.consume_identifier()
            self.consume_identifier()

            while self.tokenizer.seek().value == ",":
                self.consume_symbol(",")
                self.consume_identifier()

            self.consume_symbol(";")

    def parse_statements(self):
        with self.xml_writer.subnode("statements"):
            while self.tokenizer.seek().value != "}":
                if self.tokenizer.seek().value == "let":
                    self.parse_let()
                elif self.tokenizer.seek().value == "if":
                    self.parse_if()
                elif self.tokenizer.seek().value == "while":
                    self.parse_while()
                elif self.tokenizer.seek().value == "do":
                    self.parse_do()
                elif self.tokenizer.seek().value == "return":
                    self.parse_return()

    def parse_let(self):
        with self.xml_writer.subnode("letStatement"):
            self.consume_keyword("let")
            self.consume_identifier()
            if self.tokenizer.seek().value == "[":
                self.consume_symbol("[")
                self.parse_expression()
                self.consume_symbol("]")
            self.consume_symbol("=")
            self.parse_expression()
            self.consume_symbol(";")

    def parse_if(self):
        with self.xml_writer.subnode("ifStatement"):
            self.consume_keyword("if")
            self.consume_symbol("(")
            self.parse_expression()
            self.consume_symbol(")")
            self.consume_symbol("{")
            self.parse_statements()
            self.consume_symbol("}")
            if self.tokenizer.seek().value == "else":
                self.consume_keyword("else")
                self.consume_symbol("{")
                self.parse_statements()
                self.consume_symbol("}")

    def parse_while(self):
        with self.xml_writer.subnode("whileStatement"):
            self.consume_keyword("while")
            self.consume_symbol("(")
            self.parse_expression()
            self.consume_symbol(")")
            self.consume_symbol("{")
            self.parse_statements()
            self.consume_symbol("}")

    def parse_do(self):
        with self.xml_writer.subnode("doStatement"):
            self.consume_keyword("do")
            self.consume_identifier()
            self.parse_subroutine_call()
            self.consume_symbol(";")

    def parse_subroutine_call(self):
        if self.tokenizer.seek().value == ".":
            self.consume_symbol(".")
            self.consume_identifier()
        self.consume_symbol("(")
        self.parse_expression_list()
        self.consume_symbol(")")

    def parse_return(self):
        with self.xml_writer.subnode("returnStatement"):
            self.consume_keyword("return")
            if self.tokenizer.seek().value != ";":
                self.parse_expression()
            self.consume_symbol(";")

    def parse_expression(self):
        with self.xml_writer.subnode("expression"):
            self.parse_term()
            while self.tokenizer.seek().value in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
                self.consume_symbol("+", "-", "*", "/", "&", "|", "<", ">", "=")
                self.parse_term()

    def parse_term(self):
        with self.xml_writer.subnode("term"):
            if self.tokenizer.seek().type == Token.INT_CONST:
                self.consume_int_const()
            elif self.tokenizer.seek().type == Token.STRING_CONST:
                self.consume_string_const()
            elif self.tokenizer.seek().value in ["true", "false", "null", "this"]:
                self.consume_keyword_constant()
            elif self.tokenizer.seek().value == "(":
                self.consume_symbol("(")
                self.parse_expression()
                self.consume_symbol(")")
            elif self.tokenizer.seek().value in ["-", "~"]:
                self.consume_symbol("-", "~")
                self.parse_term()
            else:
                self.consume_identifier()
                if self.tokenizer.seek().value == "[":
                    self.consume_symbol("[")
                    self.parse_expression()
                    self.consume_symbol("]")
                elif self.tokenizer.seek().value in ["(", "."]:
                    self.parse_subroutine_call()

    def parse_expression_list(self):
        with self.xml_writer.subnode("expressionList"):
            if self.tokenizer.seek().value != ")":
                self.parse_expression()
                while self.tokenizer.seek().value == ",":
                    self.consume_symbol(",")
                    self.parse_expression()

    def write(self):
        st = ET.tostring(self.root, encoding="utf8", method="xml").decode("utf8")

        self.stream.write(
            re.sub("\n(.*) *</(symbol)>", "\\1</\\2>",re.sub("\n(.*) *</(keyword)>", "\\1</\\2>",re.sub("\n(.*) *</(integerConstant)>", "\\1</\\2>",re.sub("\n(.*) *</(stringConstant)>", "\\1</\\2>",re.sub("\n(.*) *</(identifier)>", "\\1</\\2>", re.sub("</([a-zA-Z0-9_\- ]*)>", "</\\1>\n", re.sub("<([a-zA-Z0-9_\- ]*)>", "<\\1>\n", re.sub("<([a-zA-Z\-_0-9 ]*)/>", "<\\1></\\1>", st.replace("<?xml version='1.0' encoding='utf8'?>\n", ""))))))))))
