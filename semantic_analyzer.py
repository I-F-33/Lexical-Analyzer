from tokens.token import *

class Node:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children or []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.name) + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret
    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.name) + "\n"
        for child in self.children:
            if isinstance(child, Node):
                ret += child.__repr__(level + 1)
            else:
                ret += "\t" * (level + 1) + repr(child) + "\n"
        return ret


class SyntaxTree:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]
        self.stack = []

    def match(self, token_class):
        if isinstance(self.current_token, token_class):
            matched_token = Node(f"Token({self.current_token})")
            self.advance()
            while isinstance(self.current_token, Comment):
                self.advance()
            return matched_token
        else:
            self.error(f"Expected {token_class.__name__}, but got {type(self.current_token).__name__}")

    def advance(self):
        if self.current_token_index < len(self.tokens) - 1:
            self.current_token_index += 1
            self.current_token = self.tokens[self.current_token_index]

    def error(self, message):
        raise Exception(f"Syntax Error: {message}")

    def parse_program(self):
        node = Node("program")
        if isinstance(self.current_token, Basic):
            node.add_child(self.match(Basic))
            node.add_child(self.match(Main))
            node.add_child(self.match(Left_paren))
            node.add_child(self.match(Right_paren))
            node.add_child(self.parse_block())
        else:
            node.add_child(self.parse_block())
        return node

    def parse_block(self):
        node = Node("block")
        node.add_child(self.match(Left_brace))
        node.add_child(self.parse_block_double_prime())
        node.add_child(self.match(Right_brace))
        return node

    def parse_block_double_prime(self):
        node = Node("block''")
        if isinstance(self.current_token, Basic):
            node.add_child(self.parse_decl())
            node.add_child(self.parse_block_prime())
        else:
            node.add_child(self.parse_stmts())
            node.add_child(self.parse_block_prime())
        return node

    def parse_block_prime(self):
        node = Node("block'")
        if isinstance(self.current_token, Right_brace):
            return node  # Epsilon rule
        node.add_child(self.parse_stmt())
        node.add_child(self.parse_stmts())
        node.add_child(self.match(Right_brace))
        return node

    def parse_decl(self):
        node = Node("decl")
        node.add_child(self.parse_type())
        node.add_child(self.match(Identifier))
        node.add_child(self.match(Semicolon))
        return node

    def parse_type(self):
        node = Node("type")
        node.add_child(self.match(Basic))
        node.add_child(self.parse_type_prime())
        return node

    def parse_type_prime(self):
        node = Node("type'")
        if isinstance(self.current_token, Left_bracket):
            node.add_child(self.match(Left_bracket))
            node.add_child(self.match(Number))
            node.add_child(self.match(Right_bracket))
            node.add_child(self.parse_type_prime())
        return node

    def parse_stmts(self):
        node = Node("stmts")
        if isinstance(self.current_token, (If, While, Do, Return, Break, Left_brace, Identifier)):
            node.add_child(self.parse_stmt())
            node.add_child(self.parse_stmts())
        return node

    def parse_stmt(self):
        node = Node("stmt")
        if isinstance(self.current_token, If):
            node.add_child(self.parse_if_stmt())
        elif isinstance(self.current_token, While):
            node.add_child(self.match(While))
            node.add_child(self.match(Left_paren))
            node.add_child(self.parse_bool())
            node.add_child(self.match(Right_paren))
            node.add_child(self.parse_stmt())
        elif isinstance(self.current_token, Do):
            node.add_child(self.match(Do))
            node.add_child(self.parse_stmt())
            node.add_child(self.match(While))
            node.add_child(self.match(Left_paren))
            node.add_child(self.parse_bool())
            node.add_child(self.match(Right_paren))
            node.add_child(self.match(Semicolon))
        elif isinstance(self.current_token, Return):
            node.add_child(self.match(Return))
            node.add_child(self.match(Number))
            node.add_child(self.match(Semicolon))
        elif isinstance(self.current_token, Break):
            node.add_child(self.match(Break))
            node.add_child(self.match(Semicolon))
        elif isinstance(self.current_token, Left_brace):
            node.add_child(self.parse_block())
        elif isinstance(self.current_token, Identifier):
            node.add_child(self.parse_loc())
            node.add_child(self.match(Assignment))
            node.add_child(self.parse_bool())
            node.add_child(self.match(Semicolon))
        return node

    def parse_if_stmt(self):
        node = Node("if_stmt")
        node.add_child(self.match(If))
        node.add_child(self.match(Left_paren))
        node.add_child(self.parse_bool())
        node.add_child(self.match(Right_paren))
        node.add_child(self.parse_stmt())
        if isinstance(self.current_token, Else):
            node.add_child(self.match(Else))
            node.add_child(self.parse_stmt())
        return node

    def parse_loc(self):
        node = Node("loc")
        node.add_child(self.match(Identifier))
        node.add_child(self.parse_loc_prime())
        return node

    def parse_loc_prime(self):
        node = Node("loc_prime")
        if isinstance(self.current_token, Left_bracket):
            node.add_child(self.match(Left_bracket))
            node.add_child(self.parse_bool())
            node.add_child(self.match(Right_bracket))
            node.add_child(self.parse_loc_prime())
        return node

    def parse_bool(self):
        node = Node("bool")
        node.add_child(self.parse_join())
        node.add_child(self.parse_bool_prime())
        return node

    def parse_bool_prime(self):
        node = Node("bool_prime")
        if isinstance(self.current_token, Logic_or):
            node.add_child(self.match(Logic_or))
            node.add_child(self.parse_join())
            node.add_child(self.parse_bool_prime())
        return node

    def parse_join(self):
        node = Node("join")
        node.add_child(self.parse_equality())
        node.add_child(self.parse_join_prime())
        return node

    def parse_join_prime(self):
        node = Node("join_prime")
        if isinstance(self.current_token, Logic_and):
            node.add_child(self.match(Logic_and))
            node.add_child(self.parse_equality())
            node.add_child(self.parse_join_prime())
        return node

    def parse_equality(self):
        node = Node("equality")
        node.add_child(self.parse_rel())
        node.add_child(self.parse_equality_prime())
        return node

    def parse_equality_prime(self):
        node = Node("equality_prime")
        if isinstance(self.current_token, Logic_equal):
            node.add_child(self.match(Logic_equal))
            node.add_child(self.parse_rel())
        elif isinstance(self.current_token, Logical_not_equal):
            node.add_child(self.match(Logical_not_equal))
            node.add_child(self.parse_rel())
        return node

    def parse_rel(self):
        node = Node("rel")
        node.add_child(self.parse_expr())
        node.add_child(self.parse_rel_prime())
        return node

    def parse_rel_prime(self):
        node = Node("rel_prime")
        if isinstance(self.current_token, (Less_than, Less_than_eq, Greater_than_eq, Greater_than)):
            node.add_child(self.match(type(self.current_token)))
            node.add_child(self.parse_expr())
        return node

    def parse_expr(self):
        node = Node("expr")
        node.add_child(self.parse_term())
        node.add_child(self.parse_expr_prime())
        return node

    def parse_expr_prime(self):
        node = Node("expr_prime")
        if isinstance(self.current_token, (Plus, Minus)):
            node.add_child(self.match(type(self.current_token)))
            node.add_child(self.parse_term())
            node.add_child(self.parse_expr_prime())
        return node

    def parse_term(self):
        node = Node("term")
        node.add_child(self.parse_unary())
        node.add_child(self.parse_term_prime())
        return node

    def parse_term_prime(self):
        node = Node("term_prime")
        if isinstance(self.current_token, (Multiply, Divide)):
            node.add_child(self.match(type(self.current_token)))
            node.add_child(self.parse_unary())
            node.add_child(self.parse_term_prime())
        return node

    def parse_unary(self):
        node = Node("unary")
        if isinstance(self.current_token, (Logic_not, Minus)):
            node.add_child(self.match(type(self.current_token)))
            node.add_child(self.parse_unary())
        else:
            node.add_child(self.parse_factor())
        return node

    def parse_factor(self):
        node = Node("factor")
        if isinstance(self.current_token, Left_paren):
            node.add_child(self.match(Left_paren))
            node.add_child(self.parse_bool())
            node.add_child(self.match(Right_paren))
        elif isinstance(self.current_token, Identifier):
            node.add_child(self.parse_loc())
        elif isinstance(self.current_token, (Number, Real, True, False)):
            node.add_child(self.match(type(self.current_token)))
        else:
            self.error("Expected a factor (expression, identifier, number, etc.)")
        return node

    def parse_while(self):
        node = Node("while")
        node.add_child(self.match(While))
        node.add_child(self.match(Left_paren))
        node.add_child(self.parse_bool())
        node.add_child(self.match(Right_paren))
        node.add_child(self.match(Semicolon))  # Add semicolon after Right_paren
        node.add_child(self.parse_stmt())
        return node

    def parse(self):
        self.stack.append('$')
        cst = self.parse_program()
        return cst
