import os
import sys

from lexer import Lexer
from parser import Parser, ParseError
from interpreter import Interpreter
from codegen import CodeGen

def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: python3 src/run.py <source-file> [--asm]")
        sys.exit(1)

    src_arg = None
    emit_asm = False

    for a in args:
        if a == "--asm":
            emit_asm = True
        elif src_arg is None:
            src_arg = a
        else:
            print(f"Unexpected argument: {a}")
            print("Usage: python3 src/run.py <source-file> [--asm]")
            sys.exit(1)

    if src_arg is None:
        print("Usage: python3 src/run.py <source-file> [--asm]")
        sys.exit(1)

    # build path relative to this file
    here = os.path.dirname(__file__)
    src_path = os.path.join(here, "..", src_arg)

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

    # 3) optionally generate pseudo-assembly
    if emit_asm:
        cg = CodeGen()
        asm_lines = cg.generate(ast)
        print("TARGET CODE (3-address style):")
        for line in asm_lines:
            print(line)
        print()

    # 4) interpret
    interp = Interpreter()
    outputs = interp.eval(ast)

    if outputs:
        print("OUTPUT:")
        for line in outputs:
            print(line)

if __name__ == "__main__":
    main()
