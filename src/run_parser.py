import os
from lexer import Lexer
from parser import Parser, ParseError

here = os.path.dirname(__file__)
test_path = os.path.join(here, "..", "tests", "test1.src")

print("Reading:", os.path.abspath(test_path))

with open(test_path, "r") as f:
    text = f.read()

from pprint import pprint

tokens = Lexer(text).tokenize()
print("TOKENS:")
for t in tokens:
    print(" ", t)

print("\nPARSING...")
try:
    ast = Parser(tokens).parse()
    print("\nAST:")
    pprint(ast)
except ParseError as e:
    print("SYNTAX ERROR:", e)
