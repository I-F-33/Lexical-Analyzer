
class Parser:
    
    def __init__(self, token_stream):
        self.tokens = token_stream
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]

    def eat(self, expected_token_type):
        """Consume the current token if it matches the expected token type class."""
        if isinstance(self.current_token, expected_token_type):
            self.current_token_index += 1
            if self.current_token_index < len(self.tokens):
                self.current_token = self.tokens[self.current_token_index]
        else:
            self.error(f"Unexpected token: {self.current_token}, expected {expected_token_type}")

    def parse_program(self):
        """<program> → basic main() <block>"""
        self.eat(Basic)
        self.eat(Main)
        self.eat(Left_paren)
        self.eat(Right_paren)
        self.parse_block()

    def parse_block(self):
        """<block> → { <decls> <stmts> }"""
        self.eat(Left_brace)
        self.parse_decls()
        self.parse_stmts()
        self.eat(Right_brace)

    def parse_decls(self):
        """<decls> → <decls> <decl> | ε"""
        while isinstance(self.current_token, Basic):
            self.parse_decl()

    def parse_decl(self):
        """<decl> → <type> id ;"""
        self.parse_type()
        self.eat(Identifier)
        self.eat(Semicolon)

    def parse_type(self):
        """<type> → <type> [ num ] | basic"""
        if isinstance(self.current_token, Basic):
            self.eat(Basic)
            if isinstance(self.current_token, Left_bracket):
                self.eat(Left_bracket)
                self.eat(Number)
                self.eat(Right_bracket)

    def parse_stmts(self):
        """<stmts> → <stmts> <stmt> | ε"""
        while isinstance(self.current_token, (Identifier, If, While, Do, Break, Main, Left_brace)):
            self.parse_stmt()

    def parse_stmt(self):
        """<stmt> → <loc> = <bool> ;
                    | if ( <bool> ) <stmt>
                    | if ( <bool> ) <stmt> else <stmt>
                    | while ( <bool> ) <stmt>
                    | do <stmt> while <bool> ;
                    | break ;
                    | return num ;
                    | <block>"""
        if isinstance(self.current_token, Identifier):
            self.parse_loc()
            self.eat(Assignment)
            self.parse_bool()
            self.eat(Semicolon)
        elif isinstance(self.current_token, If):
            self.eat(If)
            self.eat(Left_paren)
            self.parse_bool()
            self.eat(Right_paren)
            self.parse_stmt()
            if isinstance(self.current_token, Else):
                self.eat(Else)
                self.parse_stmt()
        elif isinstance(self.current_token, While):
            self.eat(While)
            self.eat(Left_paren)
            self.parse_bool()
            self.eat(Right_paren)
            self.parse_stmt()
        elif isinstance(self.current_token, Do):
            self.eat(Do)
            self.parse_stmt()
            self.eat(While)
            self.eat(Left_paren)
            self.parse_bool()
            self.eat(Right_paren)
            self.eat(Semicolon)
        elif isinstance(self.current_token, Break):
            self.eat(Break)
            self.eat(Semicolon)
        elif isinstance(self.current_token, Main):
            self.eat(Main)
            self.eat(Number)
            self.eat(Semicolon)
        elif isinstance(self.current_token, Left_brace):
            self.parse_block()

    def parse_loc(self):
        """<loc> → <loc> [ <bool> ] | id"""
        self.eat(Identifier)
        if isinstance(self.current_token, Left_bracket):
            self.eat(Left_bracket)
            self.parse_bool()
            self.eat(Right_bracket)

    def parse_bool(self):
        """<bool> → <bool> || <join> | <join>"""
        self.parse_join()
        while isinstance(self.current_token, Logic_or):
            self.eat(Logic_or)
            self.parse_join()

    def parse_join(self):
        """<join> → <join> && <equality> | <equality>"""
        self.parse_equality()
        while isinstance(self.current_token, Logic_and):
            self.eat(Logic_and)
            self.parse_equality()

    def parse_equality(self):
        """<equality> → <equality> == <rel> | <equality> != <rel> | <rel>"""
        self.parse_rel()
        while isinstance(self.current_token, (Logic_equal, Logical_not_equal)):
            if isinstance(self.current_token, Logic_equal):
                self.eat(Logic_equal)
            else:
                self.eat(Logical_not_equal)
            self.parse_rel()

    def parse_rel(self):
        """<rel> → <expr> < <expr>
                    | <expr> <= <expr>
                    | <expr> >= <expr>
                    | <expr> > <expr>
                    | <expr>"""
        self.parse_expr()
        if isinstance(self.current_token, (Less_than, Less_than_eq, Greater_than, Greater_than_eq)):
            self.eat(type(self.current_token))  # Eat relational operator
            self.parse_expr()

    def parse_expr(self):
        """<expr> → <expr> + <term> | <expr> - <term> | <term>"""
        self.parse_term()
        while isinstance(self.current_token, (Plus, Minus)):
            self.eat(type(self.current_token))  # Eat plus or minus
            self.parse_term()

    def parse_term(self):
        """<term> → <term> * <unary> | <term> / <unary> | <unary>"""
        self.parse_unary()
        while isinstance(self.current_token, (Multiply, Divide)):
            self.eat(type(self.current_token))  # Eat multiply or divide
            self.parse_unary()

    def parse_unary(self):
        """<unary> → ! <unary> | - <unary> | <factor>"""
        if isinstance(self.current_token, Logic_not):
            self.eat(Logic_not)
            self.parse_unary()
        elif isinstance(self.current_token, Minus):
            self.eat(Minus)
            self.parse_unary()
        else:
            self.parse_factor()

    def parse_factor(self):
        """<factor> → ( <bool> ) | <loc> | num | real | true | false"""
        if isinstance(self.current_token, Left_paren):
            self.eat(Left_paren)
            self.parse_bool()
            self.eat(Right_paren)
        elif isinstance(self.current_token, Identifier):
            self.parse_loc()
        elif isinstance(self.current_token, (Number, Real, True, False)):
            self.eat(type(self.current_token))

    def error(self, message):
        """Raise a syntax error with the given message."""
        raise Exception(f"Syntax error: {message}")

    def parse(self):
        """Initiate parsing from the top-level production rule."""
        self.parse_program()
