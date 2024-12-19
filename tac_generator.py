# work in prog
from abstract_st import ProgramNode, AssignNode, WhileNode, BinaryOpNode, ReturnNode

class TACGenerator:
    def __init__(self):
        self.counter = 0

    def generate_tac(self, node):
        if isinstance(node, ProgramNode):
            return self.generate_tac_for_program(node)
        elif isinstance(node, AssignNode):
            return self.generate_tac_for_assign(node)
        elif isinstance(node, WhileNode):
            return self.generate_tac_for_while(node)
        elif isinstance(node, BinaryOpNode):
            return self.generate_tac_for_binary_op(node)
        elif isinstance(node, ReturnNode):
            return self.generate_tac_for_return(node)
        return []

    def generate_tac_for_program(self, node):
        tac = []
        for child in node.children:
            tac.extend(self.generate_tac(child))
        return tac

    def generate_tac_for_assign(self, node):
        var_name = node.var_name
        expression_tac = self.generate_tac(node.expression)
        tac = expression_tac
        tac.append(f"{var_name} = {expression_tac[-1]}")
        return tac

    def generate_tac_for_while(self, node):
        condition_tac = self.generate_tac(node.condition)
        body_tac = self.generate_tac(node.body)
        label_start = f"L{self.counter}"
        label_end = f"L{self.counter + 1}"
        self.counter += 2

        tac = [
            f"{label_start}:",
            *condition_tac,
            f"if {condition_tac[-1]} == 0 goto {label_end}",
            *body_tac,
            f"goto {label_start}",
            f"{label_end}:"
        ]
        return tac

    def generate_tac_for_binary_op(self, node):
        left_tac = self.generate_tac(node.left)
        right_tac = self.generate_tac(node.right)
        temp_var = f"T{self.counter}"
        self.counter += 1
        tac = left_tac + right_tac
        tac.append(f"{temp_var} = {left_tac[-1]} {node.operator} {right_tac[-1]}")
        return tac

    def generate_tac_for_return(self, node):
        return [f"return {self.generate_tac(node.value)[-1]}"]
