from lexicalanalyzer import LexicalAnalyzer
from top_down_parser import Parser
from semantic_analyzer import SyntaxTree
from abstract_st import SyntaxTreeToAST

# Define test cases
test_cases = {
    "Case 1": """int main()
{
    int myInt;
    myInt = 0;
    myInt = myInt + 1;
    return 0;
}
""",
    "Case 2": """int main(void)
{
    float myFloat; 
    int counter;
    myFloat = 0.01; 
    counter = 0;
    while (counter < 5)
    {
        counter = counter + 1;
        myFloat = myFloat * 3;
    }
    counter > myFloat;
    return 0;
}
""",
    "Case 3": """
{
    int zero;
    zero = 1;
    return 0;
}
""",
    "Case 4": """int main()
{
    int myInt = 1;
    if (myInt > 1 { myInt = myInt + 1; }
    return 0;
}
""",
    "Case 5": """int main()
{
    int counter; 
    int sum;
    counter = 0; 
    sum = 0;
    while(counter < 10)
    {
        if (sum % 2 == 0)
        {
            sum = sum + 2;
        }
        else
        {
            sum = sum + 1;
        }
        counter = counter + 1;
    }
    return 0;
}
""",
    "Case 6": """int main()
{
    int variable;
    variable = 10;
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