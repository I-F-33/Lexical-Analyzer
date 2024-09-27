import lexicalanalyzer as la
from token_lexeme import Token_Lexeme

# Case 1: Feeding the lexer a lexeme stream from a file
def test_case_1():
    lexer = la.LexicalAnalyzer()

    lexemes = [
        "Variable",   # Identifier
        "12345",      # Number
        "// This is a comment",  # Comment
        "(",          # Left Parenthesis
        ")",          # Right Parenthesis
        "[",          # Left Bracket
        "]",          # Right Bracket
        "{",          # Left Brace
        "}",          # Right Brace
        ".",          # Dot
        "+",          # Plus
        "-",          # Minus
        "*",          # Multiply
        "/",          # Divide
        "%",          # Modulus
        "<",          # Less Than
        ">",          # Greater Than
        "=",          # Assignment
        ";",          # Semicolon
        ",",          # Comma
        "++",         # Increment
        "--",         # Decrement
        "<=",         # Less Than or Equal
        ">=",         # Greater Than or Equal
        "==",         # Logic Equal
        "&&",         # Logic And
        "||",         # Logic Or
        "!",          # Logic Not
        "&",          # Bit And
        "|",          # Bit Or
    ]

    for lexeme in lexemes:
        token = lexer.get_token_for_lexeme(lexeme)
        print(f"{token} -> '{lexeme}'")


# Case 2: 
def test_case_2():
    lexer = la.LexicalAnalyzer()
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
    print(lexer.get_token_stream())

# Case 3: 
def test_case_3():
    lexer = la.LexicalAnalyzer()
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
    print(lexer.get_token_stream())

# Case 4: 
def test_case_4():
    lexer = la.LexicalAnalyzer()
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
    print(lexer.get_token_stream())

# Case 5: 
def test_case_5():
    lexer = la.LexicalAnalyzer()
    code = """
    int main() {
        int myResult = 0;
        int arraySize = 5;
        int myArray[arraySize] = {1,2,3,4,5};
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
    print(lexer.get_token_stream())


if __name__ == "__main__":
    print("Test Case 1:")
    print("TOKEN -> LEXEME\n")
    test_case_1()

    print("\nTest Case 2:")
    test_case_2()

    print("\nTest Case 3:")
    test_case_3()

    print("\nTest Case 4:")
    test_case_4()

    print("\nTest Case 5:")
    test_case_5()
