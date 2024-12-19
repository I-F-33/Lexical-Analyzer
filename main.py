import lexicalanalyzer as la
import symtable as st
from abstract_st import SyntaxTreeToAST
from tac_generator import TACGenerator
from top_down_parser import Parser  # Import the Parser class from top_down_parser

class Compiler:
    def __init__(self):
        self.syntax_tree = None  # This will be populated with the syntax tree
        self.ast = None  # This will be populated with the abstract syntax tree
        self.tac_generator = TACGenerator()

    def parse_syntax_tree(self, syntax_tree):
        # Parse the raw syntax tree into AST using SyntaxTreeToAST
        syntax_to_ast = SyntaxTreeToAST(syntax_tree)
        self.ast = syntax_to_ast.transform()

    def generate_tac(self):
        # Generate TAC for the AST
        return self.tac_generator.generate_tac(self.ast)

def main():

    lexer = la.LexicalAnalyzer()

    filename = 'code.txt'
    lexer.lex(filename)

    token_stream = lexer.get_token_stream()

    #print(token_stream)
    parser = Parser(token_stream)

    syntax_tree = parser.parse()

    # init class with the syntax tree
    compiler = Compiler()
    
    # syntax tree into AST
    compiler.parse_syntax_tree(syntax_tree)
    tac = compiler.generate_tac()

    print("Generated TAC:")
    for line in tac:
        print(line)


if __name__ == '__main__':
    main()
