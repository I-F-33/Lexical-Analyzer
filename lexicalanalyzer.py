from enum import Enum

#Global Vars Define
nextToken = 0
nextChar = ''

class Token(Enum):
    IDENTIFIER = 1
    NUMBER = 2
    COMMENT = 3
    LEFT_PAREN = 4
    RIGHT_PAREN = 5
    LEFT_BRACKET = 6
    RIGHT_BRACKET = 7
    LEFT_BRACE = 8
    RIGHT_BRACE = 9
    DOT = 10
    PLUS = 11
    MINUS = 12
    MULTIPLY = 13
    DIVIDE = 14
    MODULUS = 15
    LESS_THAN = 16
    GREATER_THAN = 17
    ASSIGNMENT = 18
    SEMICOLON = 19
    COMMA = 20
    INCREMENT = 21
    DECREMENT = 22
    LESS_THAN_EQ = 23
    GREATER_THAN_EQ = 24
    LOGIC_EQUAL = 25
    LOGIC_AND = 26
    LOGIC_OR = 27
    LOGIC_NOT = 28
    BIT_AND = 29
    BIT_OR = 30

    #print(Token.PLUS.name) print(Token.PLUS.value)

KEYWORDS = [
    'int', 'float', 'char', 'main', 'return', 'while', 'for', 'break',
    'if', 'else', 'goto', 'continue', 'switch', 'case', 'unsigned', 'void'
]

def getInput():
    return input('Enter Program:')


def lex(program):
    pass

def lookup(ch):
    EOF = -1
    global nextToken
    
    if ch == '(':
        addChar()
        nextToken = LEFT_PAREN
    elif ch == ')':
        addChar()
        nextToken = RIGHT_PAREN
    elif ch == '+':
        addChar()
        nextToken = ADD_OP
    elif ch == '-':
        addChar()
        nextToken = SUB_OP
    elif ch == '*':
        addChar()
        nextToken = MULT_OP
    elif ch == '/':
        addChar()
        nextToken = DIV_OP
    else:
        addChar()
        nextToken = EOF

    return nextToken

def addChar():
    pass

def getChar(program):
    return program.pop(0)

def getNonBlank():
    pass


def main():
    ins = getInput()

    for c in ins:
        print('\n', c)

    print('Done')


if __name__ == '__main__':
    main()



