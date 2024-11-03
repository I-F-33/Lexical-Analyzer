from lexicalanalyzer import LexicalAnalyzer 
from top_down_parser import Parser

# Case 1: Feeding the lexer a lexeme stream from a file
def test_case_1():
    lexer = LexicalAnalyzer()

    lexemes = """
    int main()
    {
            int myInt;
            myInt = 0;
            myInt = myInt + 1;
            return 0;
    }
    """

    with open("test_case_1.txt", "w") as f:
        f.write(lexemes)
    
    lexer.lex("test_case_1.txt")
    tokens = lexer.get_token_stream()

    # for token in tokens:
    #     print(token.to_string())
    
    # print("\nSymbol Table:\n")
    # lexer.print_symbol_table()

    parser = Parser(tokens)
    parser.parse()



# Case 2: 
def test_case_2():
    lexer = LexicalAnalyzer()
    code = """
    int main(void)
    {
        float myFloat; int counter;
        myFloat = 0.01; counter = 0;
        while (counter < 5)
        {
            counter = counter + 1;
            myFloat = myFloat * 3;
        }
        counter > myFloat;
        return 0;
    }
    """
    with open("test_case_2.txt", "w") as f:
        f.write(code)

    lexer.lex("test_case_2.txt")
    tokens = lexer.get_token_stream()

    # for token in tokens:
    #     print(token.to_string())
    
    # print("\nSymbol Table:\n")
    # lexer.print_symbol_table()
    
    parser = Parser(tokens)
    parser.parse()

# Case 3: 
def test_case_3():
    lexer = LexicalAnalyzer()
    code = """
    {
        int zero;
        zero = 1;
        return 0;
    }
    """
    with open("test_case_3.txt", "w") as f:
        f.write(code)

    lexer.lex("test_case_3.txt")
    tokens = lexer.get_token_stream()

    # for token in tokens:
    #     print(token.to_string())
    
    # print("\nSymbol Table:\n")
    # lexer.print_symbol_table()
    
    parser = Parser(tokens)
    parser.parse()

# Case 4: 
def test_case_4():
    lexer = LexicalAnalyzer()
    code = """
    int main()
    {
        int myInt = 1;
        if (myInt > 1 { myInt = myInt + 1; }
        return 0;
    }
    """
    with open("test_case_4.txt", "w") as f:
        f.write(code)

    lexer.lex("test_case_4.txt")
    tokens = lexer.get_token_stream()

    # for token in tokens:
    #     print(token.to_string())
    
    # print("\nSymbol Table:\n")
    # lexer.print_symbol_table()
    
    parser = Parser(tokens)
    parser.parse()

# Case 5: 
def test_case_5():
    lexer = LexicalAnalyzer()
    code = """
    int main()
    {
        int counter; int sum;
        counter = 0; sum = 0;
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
    """
    with open("test_case_5.txt", "w") as f:
        f.write(code)

    lexer.lex("test_case_5.txt")
    tokens = lexer.get_token_stream()

    # print("Token Stream:\n")
    # for token in tokens:
    #     print(token.to_string())

    # print("\nSymbol Table:\n")
    # lexer.print_symbol_table()

    parser = Parser(tokens)
    parser.parse()

def test_case_6():
    lexer = LexicalAnalyzer()
    code = """
    int main()
    {
        int variable
        variable = 10;
        return 0;
    }
    """
    with open("test_case_6.txt", "w") as f:
        f.write(code)
    
    lexer.lex("test_case_6.txt")
    tokens = lexer.get_token_stream()

    # print("Token Stream:\n")
    # for token in tokens:
    #     print(token.to_string())
    
    # print("\nSymbol Table:\n")
    # lexer.print_symbol_table()

    print("\nParsing the code:\n")
    parser = Parser(tokens)
    parser.parse()




if __name__ == "__main__":
    # print("Test Case 1:")
    # test_case_1()

    # print("\nTest Case 2:")
    # test_case_2()

    # print("\nTest Case 3:")
    # test_case_3()

    # print("\nTest Case 4:")
    # test_case_4()

    # print("\nTest Case 5:")
    # test_case_5()

    print("\nTest Case 6:")
    test_case_6()
    