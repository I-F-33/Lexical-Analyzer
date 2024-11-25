import lexicalanalyzer as la
import symtable as st

def main():
    lexer = la.LexicalAnalyzer()

    filename = 'code.txt'
    lexer.lex(filename)

    token_stream = lexer.get_token_stream()

    print(token_stream)  


if __name__ == '__main__':
    main()
