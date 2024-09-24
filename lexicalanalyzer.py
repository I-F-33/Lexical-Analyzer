import tokens as Token
import dfa as d

#Global Vars Define
nextToken = 0
nextChar = ''

#print(Token.PLUS.name) print(Token.PLUS.value)

KEYWORDS = [
    'int', 'float', 'char', 'main', 'return', 'while', 'for', 'break',
    'if', 'else', 'goto', 'continue', 'switch', 'case', 'unsigned', 'void'
]


def lex():

    with open('code.txt', 'r') as code:
        dfa = d.DFA()

        tokens = []

        for line in code:
            pos = 0
            max_pos = len(line)

            while pos < max_pos:

                c = line[pos]

                #print(c)
                pos += 1

                state = dfa.analyze(c)

                print(state)
                #if this is a space not in a comment
                if state == 31:
                    last_success_state = dfa.get_last_success_state()

                    #if there was a success state before this space
                    if last_success_state != 0:
                        tokens.append(dfa.get_token(last_success_state))
                        continue
                #if this is a special character not in the dfa
                elif state == 32:

                    last_success_state = dfa.get_last_success_state()

                    #if there was a success state before this special character
                    #mainly for identifier  preceding increment or decrement
                    if last_success_state != 0:
                        tokens.append(dfa.get_token(last_success_state))
                        continue

                    match c:
                        case '(':
                            tokens.append(Token.LEFT_PAREN.name)
                        case ')':
                            tokens.append(Token.RIGHT_PAREN.name)
                        case '[':
                            tokens.append(Token.LEFT_BRACKET.name)
                        case ']':
                            tokens.append(Token.RIGHT_BRACKET.name)
                        case '{':
                            tokens.append(Token.LEFT_BRACE.name)
                        case '}':
                            tokens.append(Token.RIGHT_BRACE.name)
                        case '.':
                            tokens.append(Token.DOT.name)
                        case '+':
                            if pos != max_pos and line[pos] == '+':
                                tokens.append(Token.INCREMENT.name)
                                pos += 1
                            else:
                                tokens.append(Token.PLUS.name)
                        case '-':
                            if pos != max_pos and line[pos] == '-':

                                tokens.append(Token.DECREMENT.name)
                                pos += 1
                            else:
                                tokens.append(Token.MINUS.name)
                        case '*':
                            tokens.append(Token.MULTIPLY.name)
                        case '/':
                            tokens.append(Token.DIVIDE.name)
                        case '%':
                            tokens.append(Token.MODULUS.name)
                        case '<':
                            if pos != max_pos and line[pos] == '=':
                                tokens.append(Token.LESS_THAN_EQ.name)
                                pos += 1
                            else:    
                                tokens.append(Token.LESS_THAN.name)
                        case '>':
                            if pos != max_pos and line[pos] == '=':
                                tokens.append(Token.GREATER_THAN_EQ.name)
                                pos += 1
                            else:
                                tokens.append(Token.GREATER_THAN.name)
                        case '=':
                            if pos != max_pos and line[pos] == '=':
                                tokens.append(Token.LOGIC_EQUAL.name)
                                pos += 1
                            else:
                                tokens.append(Token.ASSIGNMENT.name)
                        case ';':
                            tokens.append(Token.SEMICOLON.name)
                        case ',':
                            tokens.append(Token.COMMA.name)
                        case '!':
                            tokens.append(Token.LOGIC_NOT.name)
                        case '&':
                            if pos != max_pos and line[pos] == '&':
                                tokens.append(Token.LOGIC_AND.name)
                                pos += 1
                            else:
                                tokens.append(Token.BIT_AND.name)
                        case '|':
                            if pos != max_pos and line[pos] == '|':
                                tokens.append(Token.LOGIC_OR.name)
                                pos += 1
                            else:
                                tokens.append(Token.BIT_OR.name)
                        case _:
                            pass
    
    return tokens


def main():
    tokens = lex()

    print(tokens)

    


if __name__ == '__main__':
    main()



