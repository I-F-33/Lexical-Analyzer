# This file contains the SymbolTable class and the Symbol class
class SymbolTable:
    _instance = None  # create singleton instance

    def __new__(cls):
        # Ensures only one instance of SymbolTable exists
        if cls._instance is None:
            cls._instance = super(SymbolTable, cls).__new__(cls)
            cls._instance.scopes = {0: {}}  # Global scope
            cls._instance.block_counter = 0
            cls._instance.current_scope_stack = [0]
        return cls._instance

    def enter_scope(self):
        self.block_counter += 1
        self.scopes[self.block_counter] = {}
        self.current_scope_stack.append(self.block_counter)
    
    def exit_scope(self):
        if len(self.current_scope_stack) > 1:
            self.current_scope_stack.pop()
        else:
            raise Exception("Cannot exit global scope")
        

    def add_symbol(self, symbol):
        # Add symbol to the current scope
        current_scope = self.current_scope_stack[-1]
        scope_symbols = self.scopes[current_scope]

        if symbol.lexeme in scope_symbols:
            raise Exception(f"Symbol {symbol.lexeme} already exists in the current scope")
        
        symbol.block_number = current_scope
        scope_symbols[symbol.lexeme] = symbol

    def lookup(self, lexeme):
        for block_number in reversed(self.current_scope_stack):
            scope_symbols = self.scopes[block_number]
            if lexeme in scope_symbols:
                return scope_symbols[lexeme]
        raise Exception(f"Symbol {lexeme} not found in the current scope")

    def flatten(self):
        flat = {}
        for block_number, scope_symbols in self.scopes.items():
            flat.update(scope_symbols)
        return flat

    def display(self):
        for block_number, scope_symbols in self.scopes.items():
            print(f"Block {block_number}:")
            if scope_symbols:
                for symbol in scope_symbols.values():
                    print(symbol)
            else:
                print("  (No symbols in this block)")
            print("\n")
class Symbol:

    _type_counters = {}

    def __init__(self, lexeme, token_type, line_number, column, length, block_number = 0):
        self.unqiue_id = self._generate_unique_id(token_type)
        self.lexeme = lexeme
        self.token_type = token_type
        self.line_number = line_number
        self.char_start = column
        self.length = length
        self.block_number = block_number
    
    def _generate_unique_id(self, token_type):
        if token_type in self._type_counters:
            self._type_counters[token_type] += 1
        else:
            self._type_counters[token_type] = 1
        return f"{token_type}{self._type_counters[token_type]}"
    

    def __str__(self):
        return f"{self.unqiue_id} {self.lexeme} {self.token_type} Line: {self.line_number} Col: {self.char_start} Len: {self.length} Block: {self.block_number}"