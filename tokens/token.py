class Token:

    def __init__(self, token_type, lexeme = ""):
        self.token_type = token_type
        self.lexeme = lexeme
    

    def to_string(self):
        return self.token_type.name + " " + self.lexeme
    
    def get_type(self):
        return self.token_type
    
    def get_lexeme(self):
        return self.lexeme    
    
