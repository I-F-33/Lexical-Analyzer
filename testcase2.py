from lexicalanalyzer import LexicalAnalyzer

# Define the test cases
test_cases = {
    "Case 1": """
int main()
{
    int myInt;
    myInt = 0;
    myInt = myInt + 1;
    return 0;
}
""",
    "Case 2": """
int main(void)
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
    "Case 4": """
int main()
{
    int myInt = 1;
    if (myInt > 1 { myInt = myInt + 1; }
    return 0;
}
""",
    "Case 5": """
int main()
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
    "Case 6": """
int main()
{
    int variable
    variable = 10;
    return 0;
}
"""
}

# Function to run a specific test case
def run_test_case(case_name, code):
    lexer = LexicalAnalyzer()
    
    # Write the code to a file
    filename = f"{case_name.replace(' ', '_').lower()}.txt"
    with open(filename, "w") as f:
        f.write(code)
    
    # Lex the file
    lexer.lex(filename)
    tokens = lexer.get_token_stream()

    print(f"{case_name} Tokens:")
    for token in tokens:
        print(token.to_string())
    print()

if __name__ == "__main__":
    for case_name, code in test_cases.items():
        run_test_case(case_name, code)
