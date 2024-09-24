import tokens as Token
import dfa as DFA

#Global Vars Define
nextToken = 0
nextChar = ''

tokens = []

#print(Token.PLUS.name) print(Token.PLUS.value)

KEYWORDS = [
    'int', 'float', 'char', 'main', 'return', 'while', 'for', 'break',
    'if', 'else', 'goto', 'continue', 'switch', 'case', 'unsigned', 'void'
]


def lex():
    with open('code.txt', 'r') as code:
        dfa = DFA()

        increment_flag = 0
        decrement_flag = 0

        for line in code.splitlines(keepends=True):
            for c in line:
                state = dfa.analyze(c)

                #if this is a space not in a comment
                if state == 31:
                    last_success_state = dfa.get_last_success_state()
                    tokens.append(dfa.get_token(last_success_state))
                    continue
                #if this is a special character not in the dfa
                elif state == 32:
                    last_success_state = dfa.get_last_success_state()

                    #if increment or decrement then add identifier to tokens list
                    if last_success_state != 0:
                        tokens.append(dfa.get_token(last_success_state))
                    else:
                        match c:
                            case '(':
                                tokens.append(Token.LEFT_PAREN)
                            case ')':
                                tokens.append(Token.RIGHT_PAREN)
                            case '[':
                                tokens.append(Token.LEFT_BRACKET)
                            case ']':
                                tokens.append(Token.RIGHT_BRACKET)
                            case '{':
                                tokens.append(Token.LEFT_BRACE)
                            case '}':
                                tokens.append(Token.RIGHT_BRACE)
                            case '.':
                                tokens.append(Token.DOT)
                            
                    



                



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



