import re
from tokens import Token, TokenType, KEYWORDS

token_specification = [
    ("NUMBER",  r"\d+"),
    ("IDENT",   r"[A-Za-z_]\w*"),
    ("PLUS",    r"\+"),
    ("MINUS",   r"-"),
    ("STAR",    r"\*"),
    ("SLASH",   r"/"),
    ("LPAREN",  r"\("),
    ("RPAREN",  r"\)"),
    ("SEMI",    r";"),
    ("ASSIGN",  r"="),
    ("NEWLINE", r"\n"),
    ("SKIP",    r"[ \t\r]+"),
    ("MISMATCH", r"."),
]

master_pat = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_specification)
)

class Lexer:
    def __init__(self, text):
        self.text = text

    def tokenize(self):
        line = 1
        line_start = 0
        tokens = []

        for mo in master_pat.finditer(self.text):
            kind = mo.lastgroup
            lexeme = mo.group()
            col = mo.start() - line_start + 1

            if kind == "NEWLINE":
                line += 1
                line_start = mo.end()
                continue
            elif kind == "SKIP":
                continue
            elif kind == "NUMBER":
                tokens.append(Token(TokenType.NUMBER, lexeme, line, col))
            elif kind == "IDENT":
                ttype = KEYWORDS.get(lexeme, TokenType.IDENT)
                tokens.append(Token(ttype, lexeme, line, col))
            elif kind in ("PLUS","MINUS","STAR","SLASH","LPAREN","RPAREN","SEMI","ASSIGN"):
                tokens.append(Token(getattr(TokenType, kind), lexeme, line, col))
            elif kind == "MISMATCH":
                raise RuntimeError(f"Unexpected character {lexeme!r} at line {line}, col {col}")

        tokens.append(Token(TokenType.EOF, "", line, 1))
        return tokens
