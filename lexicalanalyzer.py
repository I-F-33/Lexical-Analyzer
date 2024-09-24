import tokens as t
import dfa as d


#print(t.Token.PLUS.name) print(t.Token.PLUS.value)

KEYWORDS = [
    'int', 'float', 'char', 'main', 'return', 'while', 'for', 'break',
    'if', 'else', 'goto', 'continue', 'switch', 'case', 'unsigned', 'void'
]


def lex():

    with open('code.txt', 'r') as file:
        code = file.read()
        code = code.replace("\n", "\\n")

        dfa = d.DFA()

        token_stream = []

        print(code)
        pos = 0
        max_pos = len(code)

        while pos < max_pos:

            c = code[pos]

            #print(c)
            pos += 1

            state = dfa.analyze(c)

            print(c , state)
            
            #if this is a comment check for new line
            if state == 6:
                
                
                if (pos + 1) < max_pos and code[pos] == '\\' and code[pos + 1] == 'n':
                    pos += 2
                    dfa.reset()
                    token_stream.append(t.Token.COMMENT.name)

            #if this is a space not in a comment    
            elif state == 31:
                last_success_state = dfa.get_last_success_state()

                #if there was a success state before this space
                if last_success_state != 0:
                    token_stream.append(dfa.get_token(last_success_state))
                
                dfa.reset()
                
            #if this is a special character not in the dfa
            elif state == 30:

                last_success_state = dfa.get_last_success_state()
                dfa.reset()
                #if there was a success state before this special character
                #mainly for identifier  preceding increment or decrement
                if last_success_state != 0:
                    token_stream.append(dfa.get_token(last_success_state))

                match c:
                    case '(':
                        token_stream.append(t.Token.LEFT_PAREN.name)
                    case ')':
                        token_stream.append(t.Token.RIGHT_PAREN.name)
                    case '[':
                        token_stream.append(t.Token.LEFT_BRACKET.name)
                    case ']':
                        token_stream.append(t.Token.RIGHT_BRACKET.name)
                    case '{':
                        token_stream.append(t.Token.LEFT_BRACE.name)
                    case '}':
                        token_stream.append(t.Token.RIGHT_BRACE.name)
                    case '.':
                        token_stream.append(t.Token.DOT.name)
                    case '+':
                        if pos != max_pos and code[pos] == '+':
                            token_stream.append(t.Token.INCREMENT.name)
                            pos += 1
                        else:
                            token_stream.append(t.Token.PLUS.name)
                    case '-':
                        if pos != max_pos and code[pos] == '-':

                            token_stream.append(t.Token.DECREMENT.name)
                            pos += 1
                        else:
                            token_stream.append(t.Token.MINUS.name)
                    case '*':
                        token_stream.append(t.Token.MULTIPLY.name)
                    case '/':
                        token_stream.append(t.Token.DIVIDE.name)
                    case '%':
                        token_stream.append(t.Token.MODULUS.name)
                    case '<':
                        if pos != max_pos and code[pos] == '=':
                            token_stream.append(t.Token.LESS_THAN_EQ.name)
                            pos += 1
                        else:    
                            token_stream.append(t.Token.LESS_THAN.name)
                    case '>':
                        if pos != max_pos and code[pos] == '=':
                            token_stream.append(t.Token.GREATER_THAN_EQ.name)
                            pos += 1
                        else:
                            token_stream.append(t.Token.GREATER_THAN.name)
                    case '=':
                        if pos != max_pos and code[pos] == '=':
                            token_stream.append(t.Token.LOGIC_EQUAL.name)
                            pos += 1
                        else:
                            token_stream.append(t.Token.ASSIGNMENT.name)
                    case ';':
                        token_stream.append(t.Token.SEMICOLON.name)
                    case ',':
                        token_stream.append(t.Token.COMMA.name)
                    case '!':
                        token_stream.append(t.Token.LOGIC_NOT.name)
                    case '&':
                        if pos != max_pos and code[pos] == '&':
                            token_stream.append(t.Token.LOGIC_AND.name)
                            pos += 1
                        else:
                            token_stream.append(t.Token.BIT_AND.name)
                    case '|':
                        if pos != max_pos and code[pos] == '|':
                            token_stream.append(t.Token.LOGIC_OR.name)
                            pos += 1
                        else:
                            token_stream.append(t.Token.BIT_OR.name)
                    case '\\':
                        if pos != max_pos and code[pos] == 'n':
                            pos += 1
                    case _:
                        pass

    return token_stream


def main():
    token_stream = lex()

    print(token_stream)

    


if __name__ == '__main__':
    main()



