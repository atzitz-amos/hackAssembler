from xml.etree import cElementTree as ET

from parser.syntax.Tokenizer import Token


class parseEngine:
    def __init__(self, tokenizer, stream):
        self.tokenizer = tokenizer
        self.stream = stream

        print(self.tokenizer.seek())

    def eat(self, token_type):
        s = self.tokenizer.advance()
        if s != token_type:
            raise Exception(f"Expected {token_type}, got {s}")
        return s

    def parse_class(self):
        self.root = ET.Element("class")
        self.consume_keyword("class")
        self.consume_identifier()
        self.consume_symbol("{")

        while self.tokenizer.seek().value != "}":
            if self.tokenizer.seek().value == "static" or self.tokenizer.seek().value == "field":
                self.compile_class_var_dec()
            elif self.tokenizer.seek().value in ["constructor", "function", "method"]:
                self.compile_subroutine()

    def consume_keyword(self, name):
        assert self.eat(Token.KEYWORD) == name
        self.write_xml("keyword", name)

    def consume_symbol(self, symbol):
        assert self.eat(Token.SYMBOL) == symbol
        self.write_xml("symbol", symbol)

    def consume_identifier(self):
        self.write_xml("identifier", self.eat(Token.IDENTIFIER).value)

    def write_xml(self, key, value):
        ET.SubElement(self.root, key).text = value

    def compile_class_var_dec(self):
        pass

    def compile_subroutine(self):
        pass

    def compile_parameter_list(self):
        pass

    def compile_subroutine_body(self):
        pass

    def compile_var_dev(self):
        pass

    def compile_statements(self):
        pass

    def compile_let(self):
        pass

    def compile_if(self):
        pass

    def compile_while(self):
        pass

    def compile_do(self):
        pass

    def compile_return(self):
        pass

    def compile_expression(self):
        pass

    def compile_term(self):
        pass

    def compile_expression_list(self):
        pass
