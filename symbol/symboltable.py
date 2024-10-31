# This file contains the SymbolTable class and the Symbol class
class SymbolTable:
    _instance = None  # create singleton instance
    _counter = 0

    def __new__(cls):
        # Ensures only one instance of SymbolTable exists
        if cls._instance is None:
            cls._instance = super(SymbolTable, cls).__new__(cls)
            cls._instance.table = {}  # Initialize the symbol table
        return cls._instance

    def add_symbol(self, symbol):
        SymbolTable._counter += 1
        self.table[SymbolTable._counter] = symbol


    def lookup(self, lexeme):
        # Search for the symbol by lexeme in the table
        for symbol in self.table.values():
            if symbol.lexeme == lexeme:
                return symbol
        return None

    def display(self):
        for symbol in self.table.values():
            print(symbol)

class Symbol:

    _type_counters = {}

    def __init__(self, lexeme, token_type, line_number, char_start, length):
        self.unqiue_id = self._generate_unique_id(token_type)
        self.lexeme = lexeme
        self.token_type = token_type
        self.line_number = line_number
        self.char_start = char_start
        self.length = length
    
    def _generate_unique_id(self, token_type):
        if token_type in self._type_counters:
            self._type_counters[token_type] += 1
        else:
            self._type_counters[token_type] = 1
        return f"{token_type}{self._type_counters[token_type]}"
    

    def __str__(self):
        return f"{self.unqiue_id} {self.lexeme} {self.token_type} {self.line_number} {self.char_start} {self.length}"