from symbol import Symbol

class SymbolTable:
    _instance = None  # create singleton instance

    def __new__(cls):
        # Ensures only one instance of SymbolTable exists
        if cls._instance is None:
            cls._instance = super(SymbolTable, cls).__new__(cls)
            cls._instance.table = []  # Initialize the symbol table
        return cls._instance

    def add_symbol(self):
        self.table.append(Symbol)


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