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
        self.parse_block_double_prime()
        self.match(Right_brace)
        self.pop_stack()

    def parse_block_double_prime(self):
        """ Matches the rules of Block'' """
        self.stack.append("block''")
        if isinstance(self.current_token, Basic):
            self.parse_decl()
            self.parse_block_prime()
        else:
            self.parse_stmts()
            self.parse_block_prime()
        self.pop_stack()

    def parse_block_prime(self):
        """ Matches the rules of Block' """
        self.stack.append("block'")
        if isinstance(self.current_token, Right_brace):
            return  # Epsilon rule
        self.parse_stmt()
        self.parse_stmts()
        self.match(Right_brace)
        self.pop_stack()

    def parse_decls(self):
        self.stack.append("decls")
        if isinstance(self.current_token, Basic):
            self.parse_decl()
            self.parse_decls_prime()
        self.pop_stack()

    def parse_decl(self):
        self.stack.append("decl")
        self.parse_type()
        self.match(Identifier)
        self.match(Semicolon)
        self.pop_stack()

    def parse_decls_prime(self):
        self.stack.append("decls'")
        if isinstance(self.current_token, Basic):
            self.parse_decl()
            self.parse_decls_prime()
        self.pop_stack()

    def parse_type(self):
        self.stack.append("type")
        self.match(Basic)
        self.parse_type_prime()
        self.pop_stack()

    def parse_type_prime(self):
        self.stack.append("type'")
        if isinstance(self.current_token, Left_bracket):
            self.match(Left_bracket)
            self.match(Number)
            self.match(Right_bracket)
            self.parse_type_prime()
        self.pop_stack()

    def parse_stmts(self):
        self.stack.append("stmts")
        if isinstance(self.current_token, (If, While, Do, Return, Break, Left_brace, Identifier)):
            self.parse_stmt()
            self.parse_stmts()
        else:
            self.pop_stack()  # Epsilon rule

    def parse_stmt(self):
        self.stack.append("stmt")
        if isinstance(self.current_token, If):
            self.parse_if_stmt()
        elif isinstance(self.current_token, While):
            self.match(While)
            self.match(Left_paren)
            self.parse_bool()
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
        elif isinstance(self.current_token, Return):
            self.match(Return)
            self.match(Number)
            self.match(Semicolon)
        elif isinstance(self.current_token, Break):
            self.match(Break)
            self.match(Semicolon)
        elif isinstance(self.current_token, Left_brace):
            self.parse_block()
        elif isinstance(self.current_token, Identifier):
            self.parse_loc()
            self.match(Assignment)
            self.parse_bool()
            self.match(Semicolon)
        self.pop_stack()

    def parse_if_stmt(self):
        self.stack.append("if_stmt")
        self.match(If)
        self.match(Left_paren)
        self.parse_bool()
        self.match(Right_paren)
        self.parse_stmt()
        if isinstance(self.current_token, Else):
            self.match(Else)
            self.parse_stmt()
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
        elif isinstance(self.current_token, Logical_not_equal):
            self.match(Logical_not_equal)
            self.parse_rel()
        self.pop_stack()

    def parse_rel(self):
        self.stack.append("rel")
        self.parse_expr()
        self.parse_rel_prime()
        self.pop_stack()

    def parse_rel_prime(self):
        self.stack.append("rel_prime")
        if isinstance(self.current_token, (Less_than, Less_than_eq, Greater_than_eq, Greater_than)):
            self.match(type(self.current_token))
            self.parse_expr()
        self.pop_stack()

    def parse_expr(self):
        self.stack.append("expr")
        self.parse_term()
        self.parse_expr_prime()
        self.pop_stack()

    def parse_expr_prime(self):
        self.stack.append("expr_prime")
        if isinstance(self.current_token, (Plus, Minus)):
            self.match(type(self.current_token))
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
        if isinstance(self.current_token, (Multiply, Divide)):
            self.match(type(self.current_token))
            self.parse_unary()
            self.parse_term_prime()
        self.pop_stack()

    def parse_unary(self):
        self.stack.append("unary")
        if isinstance(self.current_token, (Logic_not, Minus)):
            self.match(type(self.current_token))
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
        elif isinstance(self.current_token, (Number, Real, True, False)):
            self.match(type(self.current_token))
        else:
            self.error("Expected a factor (expression, identifier, number, etc.)")
        self.pop_stack()

    def parse(self):
        self.stack.append('$')
        self.parse_program()
        print("Parsing successful.")