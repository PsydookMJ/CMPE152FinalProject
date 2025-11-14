import os
from lexer import Lexer

# Path to test file
here = os.path.dirname(__file__)
test_path = os.path.join(here, "..", "tests", "test1.src")

with open(test_path) as f:
    text = f.read()

tokens = Lexer(text).tokenize()
for t in tokens:
    print(t)
