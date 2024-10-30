from tokens.token_type import Token_type

class Token:

    def __init__(self, token_type):
        self.token_type = token_type    

    def to_string(self):
        return self.token_type.name
    
    def get_type(self):
        return self.token_type
    


class Identifier(Token):

    def __init__(self, value):
        super().__init__(Token_type.IDENTIFIER)
        self.value = value
    
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{super().get_type().name}({self.value})"

class Number(Token):
    
    def __init__(self, value):
        super().__init__(Token_type.NUMBER)
        self.value = value
    
    def __str__(self):
            return str(self.value)

    def __repr__(self):
        return f"{super().get_type().name}({self.value})"

class Comment(Token):
         
    def __init__(self):
        super().__init__(Token_type.COMMENT)
    
    def __str__(self):
        return super().get_type().name
    
    def __repr__(self):
        return f"{super().get_type().name}"

class Left_paren(Token):

    def __init__(self):
        super().__init__(Token_type.LEFT_PAREN)
    
    def __str__(self):
        return "("
    
    def __repr__(self):
        return f"{super().get_type().name}"


class Right_paren(Token):
     
    def __init__(self):
        super().__init__(Token_type.RIGHT_PAREN)
    
    def __str__(self):
        return ")"
    
    def __repr__(self):
        return f"{super().get_type().name}"
        

class Left_bracket(Token):
        
    def __init__(self):
        super().__init__(Token_type.LEFT_BRACKET)
    
    def __str__(self):
        return "["
    
    def __repr__(self):
        return f"{super().get_type().name}"
        

class Right_bracket(Token):
            
    def __init__(self):
        super().__init__(Token_type.RIGHT_BRACKET)
    
    def __str__(self):
        return "]"
    
    def __repr__(self):
        return f"{super().get_type().name}"


class Left_brace(Token):
            
    def __init__(self):
        super().__init__(Token_type.LEFT_BRACE)
            
    def __str__(self):
        return "{"
    
    def __repr__(self):
        return f"{super().get_type().name}"
            

class Right_brace(Token):
                
    def __init__(self):
        super().__init__(Token_type.RIGHT_BRACE)
                
    def __str__(self):
        return "}"
    
    def __repr__(self):
        return f"{super().get_type().name}"

class Dot(Token):
      
    def __init__(self):
        super().__init__(Token_type.DOT)
        
    def __str__(self):
        return "."
    
    def __repr__(self):
        return f"{super().get_type().name}"


class Plus(Token):
            
    def __init__(self):
        super().__init__(Token_type.PLUS)
            
    def __str__(self):
        return "+"
    
    def __repr__(self):
        return f"{super().get_type().name}"

class Minus(Token):
                
    def __init__(self):
        super().__init__(Token_type.MINUS)
                
    def __str__(self):
        return "-"
    
    def __repr__(self):
        return f"{super().get_type().name}"


class Multiply(Token):
                    
    def __init__(self):
        super().__init__(Token_type.MULTIPLY)
                    
    def __str__(self):
        return "*"
    
    def __repr__(self):
        return f"{super().get_type().name}"


class Divide(Token):
                        
    def __init__(self):
        super().__init__(Token_type.DIVIDE)
                        
    def __str__(self):
        return "/"
    
    def __repr__(self):
        return f"{super().get_type().name}"
    

class Modulus(Token):
                            
    def __init__(self):
        super().__init__(Token_type.MODULUS)
                            
    def __str__(self):
        return "%"
    
    def __repr__(self):
        return f"{super().get_type().name}"


class Less_than(Token):
                                
    def __init__(self):
        super().__init__(Token_type.LESS_THAN)
                                
    def __str__(self):
        return "<"
    
    def __repr__(self):
        return f"{super().get_type().name}"


class Greater_than(Token):
                                    
    def __init__(self):
        super().__init__(Token_type.GREATER_THAN)
                                    
    def __str__(self):
        return ">"
    
    def __repr__(self):
        return f"{super().get_type().name}"


class Assignment(Token):
                                        
    def __init__(self):
        super().__init__(Token_type.ASSIGNMENT)
                                        
    def __str__(self):
        return "="
    
    def __repr__(self):
        return f"{super().get_type().name}"
    

class Semicolon(Token):
                                            
    def __init__(self):
        super().__init__(Token_type.SEMICOLON)
                                            
    def __str__(self):
        return ";"
    
    def __repr__(self):
        return f"{super().get_type().name}"


class Comma(Token):
                                                
    def __init__(self):
        super().__init__(Token_type.COMMA)
                                                
    def __str__(self):
        return ","
    
    def __repr__(self):
        return f"{super().get_type().name}"


class Increment(Token):
                                                    
    def __init__(self):
        super().__init__(Token_type.INCREMENT)
                                                    
    def __str__(self):
        return "++"
    
    def __repr__(self):
        return f"{super().get_type().name}"
    

class Decrement(Token):
                                                        
    def __init__(self):
        super().__init__(Token_type.DECREMENT)
                                                        
    def __str__(self):
        return "--"
    
    def __repr__(self):
        return f"{super().get_type().name}"


class Less_than_eq(Token):
                                                            
    def __init__(self):
        super().__init__(Token_type.LESS_THAN_EQ)
                                                            
    def __str__(self):
        return "<="
    
    def __repr__(self):
        return f"{super().get_type().name}"


class Greater_than_eq(Token):
                                                                
    def __init__(self):
        super().__init__(Token_type.GREATER_THAN_EQ)
                                                                
    def __str__(self):
        return ">="
    
    def __repr__(self):
        return f"{super().get_type().name}"


class Logic_equal(Token):

    def __init__(self):
        super().__init__(Token_type.LOGIC_EQUAL)
    
    def __str__(self):
        return "=="

    def __repr__(self):
        return f"{super().get_type().name}"

class Logic_and(Token):

    def __init__(self):
        super().__init__(Token_type.LOGIC_AND)
    
    def __str__(self):
        return "&&"
    
    def __repr__(self):
        return f"{super().get_type().name}"


class Logic_or(Token):

    def __init__(self):
        super().__init__(Token_type.LOGIC_OR)
    
    def __str__(self):
        return "||"
    
    def __repr__(self):
        return f"{super().get_type().name}"


class Logic_not(Token):

    def __init__(self):
        super().__init__(Token_type.LOGIC_NOT)
    
    def __str__(self):
        return "!"
    
    def __repr__(self):
        return f"{super().get_type().name}"
    

class Bit_and(Token):

    def __init__(self):
        super().__init__(Token_type.BIT_AND)
    
    def __str__(self):
        return "&"
    
    def __repr__(self):
        return f"{super().get_type().name}"
    

class Bit_or(Token):

    def __init__(self):
        super().__init__(Token_type.BIT_OR)
    
    def __str__(self):
        return "|"
    
    def __repr__(self):
        return f"{super().get_type().name}"


class Basic(Token):

    def __init__(self, value):
        super().__init__(Token_type.BASIC)
        self.value = value
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return f"{super().get_type().name}({self.value})"


class If(Token):

    def __init__(self):
        super().__init__(Token_type.IF)
        
    def __str__(self):
        return "if"
    
    def __repr__(self):
        return f"{super().get_type().name}"
    

class Else(Token):

    def __init__(self):
        super().__init__(Token_type.ELSE)
    
    def __str__(self):
        return "else"
    
    def __repr__(self):
        return f"{super().get_type().name}"
    

class While(Token):

    def __init__(self):
        super().__init__(Token_type.WHILE)
    
    def __str__(self):
        return "while"
    
    def __repr__(self):
        return f"{super().get_type().name}"


class Break(Token):

    def __init__(self):
        super().__init__(Token_type.BREAK)
    
    def __str__(self):
        return "break"
    
    def __repr__(self):
        return f"{super().get_type().name}"
    

class Main(Token):

    def __init__(self):
        super().__init__(Token_type.MAIN)
    
    def __str__(self):
        return "main"

    def __repr__(self):
        return f"{super().get_type().name}"


class Do(Token):

    def __init__(self):
        super().__init__(Token_type.DO)
    
    def __str__(self):
        return "do"

    def __repr__(self):
        return f"{super().get_type().name}"


class Logical_not_equal(Token):

    def __init__(self):
        super().__init__(Token_type.LOGICAL_NOT_EQUAL)
    
    def __str__(self):
        return "!="
    
    def __repr__(self):
        return f"{super().get_type().name}"
    

class Real(Token):

    def __init__(self, value):
        super().__init__(Token_type.REAL)
        self.value = value
    
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{super().get_type().name}({self.value})"