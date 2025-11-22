from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    LPAREN = auto()
    RPAREN = auto()
    SEMI = auto()
    ASSIGN = auto()
    IDENT = auto()
    NUMBER = auto()
    PRINT = auto()
    EOF = auto()

KEYWORDS = {
    "print": TokenType.PRINT
}

@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    col: int

    def __repr__(self):
        return f"Token({self.type.name}, {self.lexeme!r}, line={self.line}, col={self.col})"
