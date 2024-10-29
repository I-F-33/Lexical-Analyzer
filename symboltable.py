class SymbolTable:
    _instance = None  # create singleton instance

    def __new__(cls):
        # Ensures only one instance of SymbolTable exists
        if cls._instance is None:
            cls._instance = super(SymbolTable, cls).__new__(cls)
            cls._instance.table = []  # Initialize the symbol table
        return cls._instance

    def add_symbol(self, lexeme, token_type, value, line_number, char_start, length):
        symbol_entry = {
            'lexeme': lexeme,
            'token_type': token_type,
            'value': value,
            'line_number': line_number,
            'char_start': char_start,
            'length': length
        }
        self.table.append(symbol_entry)

    def lookup(self, lexeme):
        for entry in self.table:
            if entry['lexeme'] == lexeme:
                return entry
        return None

    def display(self):
        print(f"{'Lexeme'}{'Token Type'}{'Value'}{'Line'}{'Start'}{'Length'}")
        for entry in self.table:
            print(f"{entry['lexeme']}{entry['token_type']}{entry['value']}"
                  f"{entry['line_number']}{entry['char_start']}{entry['length']}")