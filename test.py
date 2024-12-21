from lexicalanalyzer import LexicalAnalyzer
from top_down_parser import Parser
from semantic_analyzer import SyntaxTree
from abstract_st import SyntaxTreeToAST

# Define test cases
test_cases = {
    "Case 1": """int main()
    {
        int a = 3; int b = 5; int c;
        c = b - a;
        b = a + c;
        c = b - a;
        return 0;
    }
""",
    "Case 2": """int main()
    {
        int a = 10;
        int b = 8;
        int c;
        c = a + b;
        if (c < 20)
        {
            c = c + 5;
        }
        else
        {
            c = c - 5;
        }
        return 0;
    }
"""
}


def run_test_case(case_number, code):
    
    lexer = LexicalAnalyzer()
    filename = f"test_case_{case_number}.txt"

    # Write the code to the text files
    with open(filename, "w") as f:
        f.write(code)

    # Header for each test case
    print(f"{'='*25}\nRunning Test Case {case_number}\n{'='*25}")

    # Lex for tokens
    lexer.lex(filename)
    tokens = lexer.get_token_stream()
    lexer.print_symbol_table()

    # Output for tokens
    #print(f"Test Case {case_number} Tokens:")
    #for token in tokens:
    #    print(token.to_string())
    #print()
    
    # Concrete Syntax Tree
    parser = SyntaxTree(tokens)
    try:
        cst = parser.parse()
        print(f"Test Case {case_number} Parsed Successfully\n")
        print("Concrete Syntax Tree:")
        print(cst)
        
        # Semantic Analyzer
        semantic_analyzer = SyntaxTree(cst)
        semantic_analyzer.analyze()
        print(f"Test Case {case_number} Semantic Analysis Successful\n")

        # Abstract Syntax Tree Transformation
        transformer = SyntaxTreeToAST(cst)
        ast = transformer.transform()
        print("Abstract Syntax Tree:")
        print(ast)
        
    except Exception as e:
        print(f"Test Case {case_number} Error: {e}\n")

    # Abstract Syntax Tree


if __name__ == "__main__":
    for case_number, code in test_cases.items():
        run_test_case(case_number, code)