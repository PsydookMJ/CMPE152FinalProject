import os
from lexer import Lexer

# Build path to test file
here = os.path.dirname(__file__)
test_path = os.path.join(here, "..", "tests", "test1.src")

print("Reading file:", os.path.abspath(test_path))

with open(test_path, "r") as f:
    text = f.read()

print("FILE CONTENTS:", repr(text))

tokens = Lexer(text).tokenize()

print("\nTOKENS:")
for t in tokens:
    print(t)
