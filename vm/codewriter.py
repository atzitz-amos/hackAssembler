class CodeWriter:

    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename + (".asm" if not filename.endswith(".asm") else ""), "w+")

        self.line = 0

        self._indent = 0

    def writeline(self):
        self.file.write("\n")
        self.line += 1

    def write(self, content):
        self.file.write(self._indent * "\t" + content)
        self.writeline()

    def writeNL(self, content):
        self.file.write(content)

    def comment(self, txt):
        self.file.write(self._indent * "\t" + "// ")
        self.file.write(txt)
        self.writeline()

    def close(self):
        self.file.close()

    def indent(self):
        self._indent += 1

    def unindent(self):
        self._indent -= 1

    def bootstrap(self):
        self.write("@256")
        self.write("D=A")
        self.write("@SP")
        self.write("M=D")
