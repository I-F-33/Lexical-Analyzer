from tokens.token import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]
        self.stack = []

    def match(self, token_class):
        if isinstance(self.current_token, token_class):
            print(f"Matching {token_class.__name__}")
            print(f"Stack: {self.stack}")
            self.advance()
            while isinstance(self.current_token, Comment):
                self.advance()
            
            print(f"new token: {self.current_token}")
        else:
            self.error(f"Expected {token_class.__name__}, but got {type(self.current_token).__name__}")

    def advance(self):
        if self.current_token_index < len(self.tokens) - 1:
            self.current_token_index += 1
            self.current_token = self.tokens[self.current_token_index]

    def error(self, message):
        raise Exception(f"Syntax Error: {message}")
    
    def pop_stack(self):
        print_flag = True
        self.stack.pop()
        if print_flag:
            print(f"Stack: {self.stack}")

    def parse_program(self):
        self.stack.append("program")
        self.match(Basic)
        self.match(Main)
        self.match(Left_paren)
        self.match(Right_paren)
        self.parse_block()
        self.pop_stack()

    def parse_block(self):
        self.stack.append("block")
        self.match(Left_brace)
        self.parse_decls_stmts()
        self.match(Right_brace)
        self.pop_stack()

    def parse_decls_stmts(self):
        self.stack.append("decls_stmts")
        if isinstance(self.current_token, (Basic, Real, Number)):
            self.parse_decl()
            self.parse_decls_stmts()
        elif isinstance(self.current_token, (If, While, For, Do, Break, Continue, Return, Left_brace, Identifier)):
            self.parse_stmt()
            self.parse_decls_stmts()
        self.pop_stack()

    def parse_decl(self):
        self.stack.append("decl")
        self.parse_type()
        self.match(Identifier)
        self.parse_array_decl()
        self.parse_init()
        self.match(Semicolon)
        self.pop_stack()

    def parse_array_decl(self):
        self.stack.append("array_decl")
        if isinstance(self.current_token, Left_bracket):
            self.match(Left_bracket)
            self.parse_expr()
            self.match(Right_bracket)
        self.pop_stack()

    def parse_init(self):
        self.stack.append("init")
        if isinstance(self.current_token, Assignment):
            self.match(Assignment)
            self.parse_initializer()
        self.pop_stack()

    def parse_initializer(self):
        self.stack.append("initializer")
        if isinstance(self.current_token, Left_brace):
            self.match(Left_brace)
            self.parse_expr_list()
            self.match(Right_brace)
        else:
            self.parse_expr()
        self.pop_stack()

    def parse_expr_list(self):
        self.stack.append("expr_list")
        self.parse_expr()
        self.parse_expr_list_prime()
        self.pop_stack()

    def parse_expr_list_prime(self):
        self.stack.append("expr_list_prime")
        if isinstance(self.current_token, Comma):
            self.match(Comma)
            self.parse_expr()
            self.parse_expr_list_prime()
        self.pop_stack()

    def parse_type(self):
        self.stack.append("type")
        if isinstance(self.current_token, (Number, Real, Basic)):
            self.match(type(self.current_token))
            self.parse_type_prime()
        else:
            self.error("Expected a type (Num, Real, Basic)")
        self.pop_stack()

    def parse_type_prime(self):
        self.stack.append("type_prime")
        if isinstance(self.current_token, Left_bracket):
            self.match(Left_bracket)
            self.match(Number)
            self.match(Right_bracket)
            self.parse_type_prime()
        self.pop_stack()

    def parse_stmt(self):
        if isinstance(self.current_token, If):
            self.parse_if_stmt()
        elif isinstance(self.current_token, While):
            self.match(While)
            self.match(Left_paren)
            self.parse_bool()
            self.match(Right_paren)
            self.parse_stmt()
        elif isinstance(self.current_token, For):
            self.match(For)
            self.match(Left_paren)
            self.parse_for_init()
            self.parse_bool()
            self.match(Semicolon)
            self.parse_for_update()
            self.match(Right_paren)
            self.parse_stmt()
        elif isinstance(self.current_token, Do):
            self.match(Do)
            self.parse_stmt()
            self.match(While)
            self.match(Left_paren)
            self.parse_bool()
            self.match(Right_paren)
            self.match(Semicolon)
        elif isinstance(self.current_token, Break):
            self.match(Break)
            self.match(Semicolon)
        elif isinstance(self.current_token, Continue):
            self.match(Continue)
            self.match(Semicolon)
        elif isinstance(self.current_token, Return):
            self.match(Return)
            self.match(Number)
            self.match(Semicolon)
        elif isinstance(self.current_token, Left_brace):
            self.parse_block()
        elif isinstance(self.current_token, Identifier):
            self.parse_loc()
            if isinstance(self.current_token, Increment):
                self.match(Increment)
            elif isinstance(self.current_token, Decrement):
                self.match(Decrement)
            else:
                self.match(Assignment)
                self.parse_bool()
            self.match(Semicolon)

    def parse_if_stmt(self):
        """Parse an if statement with matched and unmatched options to handle dangling else"""
        self.stack.append("if_stmt")
        self.match(If)
        self.match(Left_paren)
        self.parse_bool()
        self.match(Right_paren)

        if isinstance(self.current_token, Else):
            self.parse_unmatched_stmt()
        else:
            self.parse_matched_stmt()

        self.pop_stack()

    def parse_matched_stmt(self):
        """<matched_stmt> → <stmt> else <stmt>"""
        self.stack.append("matched_stmt")
        self.parse_stmt()
        if isinstance(self.current_token, Else):
            self.match(Else)
            self.parse_stmt()
        self.pop_stack()

    def parse_unmatched_stmt(self):
        """<unmatched_stmt> → <stmt>"""
        self.stack.append("unmatched_stmt")
        self.parse_stmt()
        self.pop_stack()

    def parse_for_init(self):
        self.stack.append("for_init")
        if isinstance(self.current_token, Identifier):
            self.parse_loc()
            self.match(Assignment)
            self.parse_expr()
        elif isinstance(self.current_token, (Basic, Real, Number)):
            self.parse_decl()
        self.pop_stack()

    def parse_for_update(self):
        self.stack.append("for_update")
        if isinstance(self.current_token, Identifier):
            self.parse_loc()
            if isinstance(self.current_token, Increment):
                self.match(Increment)
            elif isinstance(self.current_token, Decrement):
                self.match(Decrement)
            else:
                self.match(Assignment)
                self.parse_expr()
        elif isinstance(self.current_token, (Increment, Decrement)):
            if isinstance(self.current_token, Increment):
                self.parse_increment()
            elif isinstance(self.current_token, Decrement):
                self.parse_decrement()
        else:
            self.parse_unary()
        self.pop_stack()

    def parse_loc(self):
        self.stack.append("loc")
        self.match(Identifier)
        self.parse_loc_prime()
        self.pop_stack()

    def parse_loc_prime(self):
        self.stack.append("loc_prime")
        if isinstance(self.current_token, Left_bracket):
            self.match(Left_bracket)
            self.parse_bool()
            self.match(Right_bracket)
            self.parse_loc_prime()
        self.pop_stack()

    def parse_bool(self):
        self.stack.append("bool")
        self.parse_join()
        self.parse_bool_prime()
        self.pop_stack()

    def parse_bool_prime(self):
        self.stack.append("bool_prime")
        if isinstance(self.current_token, Logic_or):
            self.match(Logic_or)
            self.parse_join()
            self.parse_bool_prime()
        self.pop_stack()

    def parse_join(self):
        self.stack.append("join")
        self.parse_equality()
        self.parse_join_prime()
        self.pop_stack()

    def parse_join_prime(self):
        self.stack.append("join_prime")
        if isinstance(self.current_token, Logic_and):
            self.match(Logic_and)
            self.parse_equality()
            self.parse_join_prime()
        self.pop_stack()

    def parse_equality(self):
        self.stack.append("equality")
        self.parse_rel()
        self.parse_equality_prime()
        self.pop_stack()

    def parse_equality_prime(self):
        self.stack.append("equality_prime")
        if isinstance(self.current_token, Logic_equal):
            self.match(Logic_equal)
            self.parse_rel()
            self.parse_equality_prime()
        elif isinstance(self.current_token, Logical_not_equal):
            self.match(Logical_not_equal)
            self.parse_rel()
            self.parse_equality_prime()
        self.pop_stack()

    def parse_rel(self):
        self.stack.append("rel")
        self.parse_expr()
        self.parse_rel_prime()
        self.pop_stack()

    def parse_rel_prime(self):
        self.stack.append("rel_prime")
        if isinstance(self.current_token, Less_than):
            self.match(Less_than)
            self.parse_expr()
        elif isinstance(self.current_token, Less_than_eq):
            self.match(Less_than_eq)
            self.parse_expr()
        elif isinstance(self.current_token, Greater_than_eq):
            self.match(Greater_than_eq)
            self.parse_expr()
        elif isinstance(self.current_token, Greater_than):
            self.match(Greater_than)
            self.parse_expr()
        elif isinstance(self.current_token, Modulus):
            self.match(Modulus)
            self.parse_expr()
        self.pop_stack()

    def parse_expr(self):
        self.stack.append("expr")
        self.parse_term()
        self.parse_expr_prime()
        self.pop_stack()

    def parse_expr_prime(self):
        self.stack.append("expr_prime")
        if isinstance(self.current_token, Plus):
            self.match(Plus)
            self.parse_term()
            self.parse_expr_prime()
        elif isinstance(self.current_token, Minus):
            self.match(Minus)
            self.parse_term()
            self.parse_expr_prime()
        self.pop_stack()

    def parse_term(self):
        self.stack.append("term")
        self.parse_unary()
        self.parse_term_prime()
        self.pop_stack()

    def parse_term_prime(self):
        self.stack.append("term_prime")
        if isinstance(self.current_token, Multiply):
            self.match(Multiply)
            self.parse_unary()
            self.parse_term_prime()
        elif isinstance(self.current_token, Divide):
            self.match(Divide)
            self.parse_unary()
            self.parse_term_prime()
        self.pop_stack()

    def parse_unary(self):
        self.stack.append("unary")
        if isinstance(self.current_token, Logic_not):
            self.match(Logic_not)
            self.parse_unary()
        elif isinstance(self.current_token, Minus):
            self.match(Minus)
            self.parse_unary()
        else:
            self.parse_factor()
        self.pop_stack()

    def parse_factor(self):
        self.stack.append("factor")
        if isinstance(self.current_token, Left_paren):
            self.match(Left_paren)
            self.parse_bool()
            self.match(Right_paren)
        elif isinstance(self.current_token, Identifier):
            self.parse_loc()
        elif isinstance(self.current_token, (Number, Real)):
            self.match(type(self.current_token))
        elif isinstance(self.current_token, (True, False)):
            self.match(type(self.current_token))
        else:
            self.error("Expected a factor (expression, identifier, number, etc.)")
        self.pop_stack()

    def parse(self):
        self.stack.append('$')
        self.parse_program()
        print("Parsing successful.")