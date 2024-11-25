class ASTNode:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children or []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self, level=0):
        ret = "\t" * level + f"{self.name}\n"
        for child in self.children:
            ret += child.__repr__(level + 1) if isinstance(child, ASTNode) else "\t" * (level + 1) + repr(child) + "\n"
        return ret

class ProgramNode(ASTNode):
    def __init__(self):
        super().__init__("Program")

class BlockNode(ASTNode):
    def __init__(self):
        super().__init__("Block")

class VarDeclNode(ASTNode):
    def __init__(self, var_type, var_name):
        super().__init__("VarDecl")
        self.var_type = var_type
        self.var_name = var_name

class AssignNode(ASTNode):
    def __init__(self, var_name, expression):
        super().__init__("Assign")
        self.var_name = var_name
        self.expression = expression

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        super().__init__("While")
        self.condition = condition
        self.body = body

class BinaryOpNode(ASTNode):
    def __init__(self, operator, left, right):
        super().__init__("BinaryOp")
        self.operator = operator
        self.left = left
        self.right = right

class ReturnNode(ASTNode):
    def __init__(self, value):
        super().__init__("Return")
        self.value = value

class SyntaxTreeToAST:
    def __init__(self, syntax_tree):
        self.syntax_tree = syntax_tree

    def transform(self):
        return self._transform_node(self.syntax_tree)

    def _transform_node(self, node):
        if node.name == "program":
            program_node = ProgramNode()
            for child in node.children:
                program_node.add_child(self._transform_node(child))
            return program_node

        elif node.name == "block":
            block_node = BlockNode()
            for child in node.children:
                if isinstance(child, Node):  # Skip tokens
                    block_node.add_child(self._transform_node(child))
            return block_node

        elif node.name == "decl":
            var_type = node.children[0].name  # First child is type
            var_name = node.children[1].name  # Second child is identifier
            return VarDeclNode(var_type, var_name)

        elif node.name == "stmt":
            first_child = node.children[0]
            if first_child.name == "While":
                condition = self._transform_node(node.children[2])  # Condition
                body = self._transform_node(node.children[4])       # Body
                return WhileNode(condition, body)
            elif first_child.name == "Return":
                value = self._transform_node(node.children[1])      # Value
                return ReturnNode(value)
            elif isinstance(first_child, Node) and first_child.name == "Identifier":
                var_name = first_child.name
                expression = self._transform_node(node.children[2])
                return AssignNode(var_name, expression)

        elif node.name == "expr" or node.name == "bool":
            left = self._transform_node(node.children[0])
            if len(node.children) > 1:
                operator = node.children[1].name  # Operator
                right = self._transform_node(node.children[2])
                return BinaryOpNode(operator, left, right)
            return left

        elif node.name == "factor":
            return node.children[0].name  # Could be a literal or identifier

        # Add cases for other node types as needed

        return None  # Default case for unhandled nodes
