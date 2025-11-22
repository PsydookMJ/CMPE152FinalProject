from dataclasses import dataclass
from typing import List

# ---------- Expressions ----------

@dataclass
class Expr:
    pass

@dataclass
class Number(Expr):
    value: int

@dataclass
class Var(Expr):
    name: str

@dataclass
class Unary(Expr):
    op: str
    right: Expr

@dataclass
class Binary(Expr):
    left: Expr
    op: str
    right: Expr

# ---------- Statements ----------

@dataclass
class Stmt:
    pass

@dataclass
class Assign(Stmt):
    name: str
    expr: Expr

@dataclass
class Print(Stmt):
    expr: Expr

@dataclass
class Block(Stmt):
    stmts: List[Stmt]
