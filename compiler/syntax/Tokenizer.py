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
                    while self.src[self.index] in self.NUMBERS:
                        value += self.src[self.index]
                        self.index += 1
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
    t = Tokenizer("""
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/10/Square/Main.jack

// Derived from projects/09/Square/Main.jack.
// This class is functionally the same as the original Main.class.
// But, some changes were made, in order to test the parsing capability
// of the syntax analyzer developed in project 10.
// The changes are documented in the ////comments below.   

/** Initializes a new Square Dance game and starts running it. */
class Main {

   //// The following static variable was added to the code, 
   //// to check how the syntax analyzer handles static variables.
   static boolean test;

   function void main() {
      var SquareGame game;
      let game = SquareGame.new();
      do game.run();
      do game.dispose();
      return;
   }

   //// The following function was added to the code, to check how the
   //// syntax analyzer handles various language features that don't appear
   //// in the original code.
   function void test() { 
      var int i, j;      
      var String s;
      var Array a;
      if (false) {
         let s = "string constant";
         let s = null;
         let a[1] = a[2];
      }
      else {              
         let i = i * (-j);
         let j = j / (-2);
         let i = i | j;
      }
      return;
   }
}
""")
    while True:
        token = t.advance()
        token2 = t.seek()
        if token is None or token2 is None:
            break
        print(["KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"][token.type], token.value, "--",
              ["KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"][token2.type], token2.value)
