from lexicalanalyzer import LexicalAnalyzer 

# Case 1: Feeding the lexer a lexeme stream from a file
def test_case_1():
    lexer = LexicalAnalyzer()

    lexemes = """
        Variables
        12345     
        // This is a comment
        (
        )
        [        
        ]       
        {
        }
        .
        +
        -
        *
        /
        %
        <
        >
        =
        ;
        ,
        ++
        --
        <=
        >=
        ==
        &&
        ||
        !
        &
        |
    """

    with open("test_case_1.txt", "w") as f:
        f.write(lexemes)
    
    lexer.lex("test_case_1.txt")
    tokens = lexer.get_token_stream()

    for token in tokens:
        print(token.to_string())



# Case 2: 
def test_case_2():
    lexer = LexicalAnalyzer()
    code = """
    int main() {
        int myInt = 0;
        myInt++;
        myInt << 1;
        return 0;
    }
    """
    with open("test_case_2.txt", "w") as f:
        f.write(code)

    lexer.lex("test_case_2.txt")
    tokens = lexer.get_token_stream()

    for token in tokens:
        print(token.to_string())

# Case 3: 
def test_case_3():
    lexer = LexicalAnalyzer()
    code = """
    int main() {
        int 1stint = 0;
        char myChar2;
        return 0;
    }
    """
    with open("test_case_3.txt", "w") as f:
        f.write(code)

    lexer.lex("test_case_3.txt")
    tokens = lexer.get_token_stream()

    for token in tokens:
        print(token.to_string())

# Case 4: 
def test_case_4():
    lexer = LexicalAnalyzer()
    code = """
    int main(void) {
        float myFloat = 0.01;
        int counter = 0;
        while (counter < 5) {
            ++counter;
            myFloat = myFloat * 3;
        }
        counter > myFloat;
        return 0;
    }
    """
    with open("test_case_4.txt", "w") as f:
        f.write(code)

    lexer.lex("test_case_4.txt")
    tokens = lexer.get_token_stream()

    for token in tokens:
        print(token.to_string())

# Case 5: 
def test_case_5():
    lexer = LexicalAnalyzer()
    code = """
    int main() {
        int myResult = 0;
        int arraySize = 5;
        int myArray[arraySize] = {1.2,2,3.5,4,5};
        // this is a for loop
        for (int i = 0; i < arraySize; ++i) {
            if (myArray[i] % 2 == 0) {
                myResult++;
            } else {
                myResult--;
            }
        }
        if (myResult >= 0) {
            continue;
        } else {
            myResult = myResult * (-1);
        }
        return 0;
    }
    """
    with open("test_case_5.txt", "w") as f:
        f.write(code)

    lexer.lex("test_case_5.txt")
    tokens = lexer.get_token_stream()

    for token in tokens:
        print(token.to_string())


if __name__ == "__main__":
    # print("Test Case 1:")
    # print("TOKEN -> LEXEME\n")
    # test_case_1()

    # print("\nTest Case 2:")
    # test_case_2()

    # print("\nTest Case 3:")
    # test_case_3()

    # print("\nTest Case 4:")
    # test_case_4()

    print("\nTest Case 5:")
    test_case_5()