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
        print(f"{'Lexeme':<15}{'Token Type':<15}{'Value':<15}{'Line':<10}{'Start':<10}{'Length':<10}")
        print("-" * 75)
        for entry in self.table:
            print(f"{entry['lexeme']:<15}{entry['token_type']:<15}{entry['value']:<15}"
                  f"{entry['line_number']:<10}{entry['char_start']:<10}{entry['length']:<10}")