import os
import sys

from CompileEngine import CompileEngine
from Tokenizer import Tokenizer
from VMWriter import VMWriter


def analyze(path, name):
    with open(os.path.join(path, name), "r") as reader:
        tokenizer = Tokenizer(reader.read())
        output_file = input_file_name_without_extension + ".vm"
        with open(os.path.join(path, output_file), "w") as writer:
            vmwriter = VMWriter(writer)

            compile_engine = CompileEngine(tokenizer, vmwriter)
            compile_engine.compile_class()

            vmwriter.close()


if __name__ == "__main__":
    # Prompt the user for a file path or hard-code one

    # Check if a filename was provided as a command-line argument
    if len(sys.argv) > 1:
        input_file_path = sys.argv[1]
        print(f"Filename provided: {input_file_path}")
    else:
        print("No filename provided.")
        # Optionally, exit the script if no filename is provided
        sys.exit(1)

    if os.path.isdir(input_file_path):
        for filename in os.listdir(input_file_path):
            input_file_name_without_extension, extension = os.path.splitext(filename)
            if extension == ".jack":
                analyze(input_file_path, filename)
    elif os.path.isfile(input_file_path):
        # input_file_name_without_extension, extension = os.path.splitext(input_file_path)
        analyze(input_file_path, input_file_path)
