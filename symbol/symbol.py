
class Symbol:

    def __init__(self, lexeme, token_type, value, line_number, char_start, length):
        self.lexeme = lexeme
        self.token_type = token_type
        self.value = value
        self.line_number = line_number
        self.char_start = char_start
        self.length = length
    
    def __str__(self):
        return f"{self.lexeme} {self.token_type} {self.value} {self.line_number} {self.char_start} {self.length}"
