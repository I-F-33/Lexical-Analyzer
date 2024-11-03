from tokens.token_type import Token_type

class Token:

    def __init__(self, token_type):
        self.token_type = token_type    

    def to_string(self):
        return self.token_type.name
    
    def get_type(self):
        return self.token_type.name
    


class Identifier(Token):

    def __init__(self, value):
        super().__init__(Token_type.IDENTIFIER)
        self.value = value
    
    def __str__(self):
        return str(self.value)

class Number(Token):
    
    def __init__(self, value):
        super().__init__(Token_type.NUMBER)
        self.value = value
    
    def __str__(self):
            return str(self.value)

class Comment(Token):
         
    def __init__(self):
        super().__init__(Token_type.COMMENT)
    
    def __str__(self):
        return super().get_type()

class Left_paren(Token):

    def __init__(self):
        super().__init__(Token_type.LEFT_PAREN)
    
    def __str__(self):
        return "("

class Right_paren(Token):
     
    def __init__(self):
        super().__init__(Token_type.RIGHT_PAREN)
    
    def __str__(self):
        return ")"

class Left_bracket(Token):
        
    def __init__(self):
        super().__init__(Token_type.LEFT_BRACKET)
    
    def __str__(self):
        return "["

class Right_bracket(Token):
            
    def __init__(self):
        super().__init__(Token_type.RIGHT_BRACKET)
    
    def __str__(self):
        return "]"

class Left_brace(Token):
            
    def __init__(self):
        super().__init__(Token_type.LEFT_BRACE)
            
    def __str__(self):
        return "{"

class Right_brace(Token):
                
    def __init__(self):
        super().__init__(Token_type.RIGHT_BRACE)
                
    def __str__(self):
        return "}"
    
class Dot(Token):
      
    def __init__(self):
        super().__init__(Token_type.DOT)
        
    def __str__(self):
        return "."

class Plus(Token):
            
    def __init__(self):
        super().__init__(Token_type.PLUS)
            
    def __str__(self):
        return "+"

class Minus(Token):
                
    def __init__(self):
        super().__init__(Token_type.MINUS)
                
    def __str__(self):
        return "-"

class Multiply(Token):
                    
    def __init__(self):
        super().__init__(Token_type.MULTIPLY)
                    
    def __str__(self):
        return "*"

class Divide(Token):
                        
    def __init__(self):
        super().__init__(Token_type.DIVIDE)
                        
    def __str__(self):
        return "/"

class Modulus(Token):
                            
    def __init__(self):
        super().__init__(Token_type.MODULUS)
                            
    def __str__(self):
        return "%"

class Less_than(Token):
                                
    def __init__(self):
        super().__init__(Token_type.LESS_THAN)
                                
    def __str__(self):
        return "<"

class Greater_than(Token):
                                    
    def __init__(self):
        super().__init__(Token_type.GREATER_THAN)
                                    
    def __str__(self):
        return ">"

class Assignment(Token):
                                        
    def __init__(self):
        super().__init__(Token_type.ASSIGNMENT)
                                        
    def __str__(self):
        return "="

class Semicolon(Token):
                                            
    def __init__(self):
        super().__init__(Token_type.SEMICOLON)
                                            
    def __str__(self):
        return ";"

class Comma(Token):
                                                
    def __init__(self):
        super().__init__(Token_type.COMMA)
                                                
    def __str__(self):
        return ","

class Increment(Token):
                                                    
    def __init__(self):
        super().__init__(Token_type.INCREMENT)
                                                    
    def __str__(self):
        return "++" 

class Decrement(Token):
                                                        
    def __init__(self):
        super().__init__(Token_type.DECREMENT)
                                                        
    def __str__(self):
        return "--"

class Less_than_eq(Token):
                                                            
    def __init__(self):
        super().__init__(Token_type.LESS_THAN_EQ)
                                                            
    def __str__(self):
        return "<="

class Greater_than_eq(Token):
                                                                
    def __init__(self):
        super().__init__(Token_type.GREATER_THAN_EQ)
                                                                
    def __str__(self):
        return ">="

class Logic_equal(Token):

    def __init__(self):
        super().__init__(Token_type.LOGIC_EQUAL)
    
    def __str__(self):
        return "=="

class Logic_and(Token):

    def __init__(self):
        super().__init__(Token_type.LOGIC_AND)
    
    def __str__(self):
        return "&&"
    
class Logic_or(Token):

    def __init__(self):
        super().__init__(Token_type.LOGIC_OR)
    
    def __str__(self):
        return "||"

class Logic_not(Token):

    def __init__(self):
        super().__init__(Token_type.LOGIC_NOT)
    
    def __str__(self):
        return "!"    

class Bit_and(Token):

    def __init__(self):
        super().__init__(Token_type.BIT_AND)
    
    def __str__(self):
        return "&"

class Bit_or(Token):

    def __init__(self):
        super().__init__(Token_type.BIT_OR)
    
    def __str__(self):
        return "|"

class Basic(Token):

    def __init__(self, value):
        super().__init__(Token_type.BASIC)
        self.value = value
    
    def __str__(self):
        return str(self.value)

class If(Token):

    def __init__(self):
        super().__init__(Token_type.IF)
        
    def __str__(self):
        return "if"

class Else(Token):

    def __init__(self):
        super().__init__(Token_type.ELSE)
    
    def __str__(self):
        return "else"

class While(Token):

    def __init__(self):
        super().__init__(Token_type.WHILE)
    
    def __str__(self):
        return "while"

class Break(Token):

    def __init__(self):
        super().__init__(Token_type.BREAK)
    
    def __str__(self):
        return "break"

class Main(Token):

    def __init__(self):
        super().__init__(Token_type.MAIN)
    
    def __str__(self):
        return "main"

class Do(Token):

    def __init__(self):
        super().__init__(Token_type.DO)
    
    def __str__(self):
        return "do"

class Logical_not_equal(Token):

    def __init__(self):
        super().__init__(Token_type.LOGICAL_NOT_EQUAL)
    
    def __str__(self):
        return "!="

class Real(Token):

    def __init__(self, value):
        super().__init__(Token_type.REAL)
        self.value = value
    
    def __str__(self):
        return str(self.value)
    
class Return(Token):

    def __init__(self):
        super().__init__(Token_type.RETURN)
    
    def __str__(self):
        return "return"
    
class For(Token):

    def __init__(self):
        super().__init__(Token_type.FOR)
    
    def __str__(self):
        return "for"

class Continue(Token):
    def __init__(self):
        super().__init__(Token_type.CONTINUE)
    
    def __str__(self):
        return "continue"

class Unsigned(Token):
    def __init__(self):
        super().__init__(Token_type.UNSIGNED)
    
    def __str__(self):
        return "unsigned"

class Goto(Token):
    def __init__(self):
        super().__init__(Token_type.GOTO)
    
    def __str__(self):
        return "goto"

class Case(Token):
    def __init__(self):
        super().__init__(Token_type.CASE)
    
    def __str__(self):
        return "case"

class Switch(Token):
    def __init__(self):
        super().__init__(Token_type.SWITCH)
    
    def __str__(self):
        return "switch"
