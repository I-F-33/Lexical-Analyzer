from enum import Enum 

class Token_type(Enum):
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