import re
from tokens import Token, TokenType, KEYWORDS

_specs = [
    ("NUMBER",  r'\d+'),
    ("IDENT",   r'[A-Za-z_]\w*'),
    ("PLUS",    r'\+'),
    ("MINUS",   r'-'),
    ("STAR",    r'\*'),
    ("SLASH",   r'/'),
    ("LPAREN",  r'\('),
    ("RPAREN",  r'\)'),
    ("SEMI",    r';'),
    ("ASSIGN",  r'='),
    ("WS",      r'[ \t\r]+'),
    ("NEWLINE", r'\n'),
    ("BAD",     r'.'),
]

PAT = re.compile("|".join(f"(?P<{n}>{p})" for n,p in _specs))

class Lexer:
    def __init__(self, text):
        self.text = text

    def tokenize(self):
        line = 1
        line_start = 0
        tokens = []

        for m in PAT.finditer(self.text):
            kind = m.lastgroup
            lex = m.group()
            col = m.start() - line_start + 1

            if kind == "WS":
                continue
            if kind == "NEWLINE":
                line += 1
                line_start = m.end()
                continue

            if kind == "NUMBER":
                tokens.append(Token(TokenType.NUMBER, lex, line, col))
                continue

            if kind == "IDENT":
                ttype = KEYWORDS.get(lex, TokenType.IDENT)
                tokens.append(Token(ttype, lex, line, col))
                continue

            if kind in ("PLUS","MINUS","STAR","SLASH","LPAREN","RPAREN","SEMI","ASSIGN"):
                tokens.append(Token(getattr(TokenType, kind), lex, line, col))
                continue

            raise Exception(f"Bad character '{lex}' at line {line}, col {col}")

        tokens.append(Token(TokenType.EOF, "", line, 1))
        return tokens
