import os
import sys

from lexer import Lexer
from parser import Parser, ParseError
from interpreter import Interpreter

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 src/run.py tests/test1.src")
        sys.exit(1)

    # relative path like "tests/test1.src"
    rel_path = sys.argv[1]

    here = os.path.dirname(__file__)
    src_path = os.path.join(here, "..", rel_path)

    with open(src_path, "r") as f:
        text = f.read()

    # 1) tokenize
    tokens = Lexer(text).tokenize()

    # 2) parse
    try:
        ast = Parser(tokens).parse()
    except ParseError as e:
        print("SYNTAX ERROR:", e)
        sys.exit(1)

    # 3) interpret
    interp = Interpreter()
    outputs = interp.eval(ast)

    if outputs:
        print("OUTPUT:")
        for line in outputs:
            print(line)

if __name__ == "__main__":
    main()
