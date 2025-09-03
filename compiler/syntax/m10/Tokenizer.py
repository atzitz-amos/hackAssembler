class Token:
    KEYWORD = 0
    SYMBOL = 1
    IDENTIFIER = 2
    INT_CONST = 3
    STRING_CONST = 4

    def __init__(self, type_, value):
        self.type = type_
        self.value = value


class Tokenizer:
    KEYWORDS = [
        "class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void",
        "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"
    ]

    SYMBOLS = [
        "{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"
    ]

    NUMBERS = [
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
    ]

    def __init__(self, src):
        self.src = src

        self.index = 0

        self.tokens = []
        self.currentToken = 0

    def hasMoreTokens(self):
        return self.seek() is not None

    def buildToken(self):
        cache = ""
        result = None
        while not result:
            if self.index >= len(self.src):
                if cache != "":
                    return Token(Token.KEYWORD if cache in self.KEYWORDS else Token.IDENTIFIER, cache)
                return None

            if self.src[self.index] == "/" and self.index + 1 < len(self.src):
                if self.src[self.index + 1] == "/":
                    self.index += 2
                    while self.index < len(self.src) and self.src[self.index] != "\n":
                        self.index += 1
                elif self.src[self.index + 1] == "*":
                    self.index += 2
                    while (self.index + 1 < len(self.src)
                           and not (self.src[self.index] == "*"
                                    and self.src[self.index + 1] == "/")):
                        self.index += 1
                    self.index += 2
            char = self.src[self.index]
            if char in "\n\t ":
                if cache != "":
                    return Token(Token.KEYWORD if cache in self.KEYWORDS else Token.IDENTIFIER, cache)
            elif char in self.NUMBERS:
                if cache != "":
                    cache += char
                else:
                    value = ""
                    while self.index < len(self.src) and self.src[self.index] in self.NUMBERS:
                        value += self.src[self.index]
                        self.index += 1
                    self.index -= 1
                    result = Token(Token.INT_CONST, value)
            elif char in self.SYMBOLS:
                if cache != "":
                    return Token(Token.KEYWORD if cache in self.KEYWORDS else Token.IDENTIFIER, cache)
                else:
                    result = Token(Token.SYMBOL, char)
            elif char == "\"":
                if cache != "":
                    return Token(Token.KEYWORD if cache in self.KEYWORDS else Token.IDENTIFIER, cache)
                else:
                    value = ""
                    self.index += 1
                    while self.src[self.index] != "\"":
                        value += self.src[self.index]
                        self.index += 1
                    result = Token(Token.STRING_CONST, value)
            else:
                cache += char
            self.index += 1
        return result

    def seek(self):
        while self.currentToken + 1 >= len(self.tokens):
            self.tokens.append(self.buildToken())
        return self.tokens[self.currentToken]

    def advance(self):
        tk = self.seek()
        self.currentToken += 1
        return tk


if __name__ == '__main__':
    t = Tokenizer("""a[12] = "hello";""")
    while True:
        token = t.advance()
        if token is None:
            break
        print(["KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"][token.type], token.value)
