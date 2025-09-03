class VMWriter:
    def __init__(self, output_file):
        self.output_stream = output_file

    def write_push(self, segment, index):
        self.output_stream.write("push {} {}\n".format(segment, index))

    def write_pop(self, segment, index):
        self.output_stream.write("pop {} {}\n".format(segment, index))

    def write_arithmetic(self, command):
        self.output_stream.write("{}\n".format(command))

    def write_label(self, label):
        self.output_stream.write("label {}\n".format(label))

    def write_goto(self, label):
        self.output_stream.write("goto {}\n".format(label))

    def write_if(self, label):
        self.output_stream.write("if-goto {}\n".format(label))

    def write_call(self, name, n_args):
        self.output_stream.write("call {} {}\n".format(name, n_args))

    def write_function(self, name, n_locals):
        self.output_stream.write("function {} {}\n".format(name, n_locals))

    def write_return(self):
        self.output_stream.write("return\n")

    def close(self):
        self.output_stream.close()

    def compile_class(self):
        pass

    def compile_subroutine(self):
        pass

    def compile_parameter_list(self):
        pass
