from tokens import TokenType
from nodes import Number, Var, Unary, Binary, Assign, Print, Block

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0  # current index

    # ---------- ENTRY POINT ----------
    def parse(self):
        stmts = []
        while not self._is_at_end():        # <-- FIXED HERE
            stmts.append(self.statement())
        return Block(stmts)

    # ---------- STATEMENTS ----------
    # statement -> "print" "(" expression ")" ";" | IDENT "=" expression ";"
    def statement(self):
        if self._match(TokenType.PRINT):
            self._consume(TokenType.LPAREN, "Expect '(' after print")
            expr = self.expression()
            self._consume(TokenType.RPAREN, "Expect ')' after expression")
            self._consume(TokenType.SEMI, "Expect ';' after print")
            return Print(expr)

        # assignment: IDENT "=" expression ";"
        name_tok = self._consume(TokenType.IDENT, "Expect identifier")
        self._consume(TokenType.ASSIGN, "Expect '=' after identifier")
        expr = self.expression()
        self._consume(TokenType.SEMI, "Expect ';' after assignment")
        return Assign(name_tok.lexeme, expr)

    # ---------- EXPRESSIONS ----------
    # expression -> term (("+" | "-") term)*
    def expression(self):
        expr = self.term()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            op = self._previous().lexeme
            right = self.term()
            expr = Binary(expr, op, right)
        return expr

    # term -> factor (("*" | "/") factor)*
    def term(self):
        expr = self.factor()
        while self._match(TokenType.STAR, TokenType.SLASH):
            op = self._previous().lexeme
            right = self.factor()
            expr = Binary(expr, op, right)
        return expr

    # factor -> ("+"|"-") factor | NUMBER | IDENT | "(" expression ")"
    def factor(self):
        if self._match(TokenType.PLUS, TokenType.MINUS):
            op = self._previous().lexeme
            right = self.factor()
            return Unary(op, right)

        if self._match(TokenType.NUMBER):
            return Number(int(self._previous().lexeme))

        if self._match(TokenType.IDENT):
            return Var(self._previous().lexeme)

        if self._match(TokenType.LPAREN):
            expr = self.expression()
            self._consume(TokenType.RPAREN, "Expect ')' after expression")
            return expr

        raise ParseError(f"Expect expression at token {self._peek()}")

    # ---------- HELPER METHODS ----------
    def _match(self, *types):
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _consume(self, ttype, msg):
        if self._check(ttype):
            return self._advance()
        raise ParseError(msg + f" at {self._peek()}")

    def _check(self, ttype):
        if self._is_at_end():
            return False
        return self._peek().type == ttype

    def _advance(self):
        if not self._is_at_end():
            self.i += 1
        return self._previous()

    def _is_at_end(self):
        return self._peek().type == TokenType.EOF

    def _peek(self):
        return self.tokens[self.i]

    def _previous(self):
        return self.tokens[self.i - 1]
