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

    tokens = []

    with open('code.txt', 'r') as code:
        dfa = d.DFA()

        for line in code:
            pos = 0
            max_pos = len(line)

            while pos < max_pos:

                c = line[pos]
                pos += 1

                state = dfa.analyze(c)

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
                        case '+':
                            if pos != max_pos and line[pos] == '+':
                                tokens.append(Token.INCREMENT)
                                pos += 1
                            else:
                                tokens.append(Token.PLUS)
                        case '-':
                            if pos != max_pos and line[pos] == '-':

                                tokens.append(Token.DECREMENT)
                                pos += 1
                            else:
                                tokens.append(Token.MINUS)
                        case '*':
                            tokens.append(Token.MULTIPLY)
                        case '/':
                            tokens.append(Token.DIVIDE)
                        case '%':
                            tokens.append(Token.MODULUS)
                        case '<':
                            if pos != max_pos and line[pos] == '=':
                                tokens.append(Token.LESS_THAN_EQ)
                                pos += 1
                            else:    
                                tokens.append(Token.LESS_THAN)
                        case '>':
                            if pos != max_pos and line[pos] == '=':
                                tokens.append(Token.GREATER_THAN_EQ)
                                pos += 1
                            else:
                                tokens.append(Token.GREATER_THAN)
                        case '=':
                            if pos != max_pos and line[pos] == '=':
                                tokens.append(Token.LOGIC_EQUAL)
                                pos += 1
                            else:
                                tokens.append(Token.ASSIGNMENT)
                        case ';':
                            tokens.append(Token.SEMICOLON)
                        case ',':
                            tokens.append(Token.COMMA)
                        case '!':
                            tokens.append(Token.LOGIC_NOT)
                        case '&':
                            if pos != max_pos and line[pos] == '&':
                                tokens.append(Token.LOGIC_AND)
                                pos += 1
                            else:
                                tokens.append(Token.BIT_AND)
                        case '|':
                            if pos != max_pos and line[pos] == '|':
                                tokens.append(Token.LOGIC_OR)
                                pos += 1
                            else:
                                tokens.append(Token.BIT_OR)
                        case _:
                            pass
    
    return tokens


def main():
    tokens = lex()
    
    


if __name__ == '__main__':
    main()



