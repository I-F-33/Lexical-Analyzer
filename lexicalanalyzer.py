import tokens as t
import dfa as d

class LexicalAnalyzer:

    def __init__(self):
        self.dfa = d.DFA()
        self.keywords = [
        'int', 'float', 'char', 'main', 'return', 'while', 'for', 'break',
        'if', 'else', 'goto', 'continue', 'switch', 'case', 'unsigned', 'void'
        ]
        self.token_stream = []


    def lex(self, filename):

        with open(filename, 'r') as file:
            code = file.read()
            code = code.replace("\n", "\\n")

            pos = 0
            max_pos = len(code)

            while pos < max_pos:

                c = code[pos]
                pos += 1

                state = self.dfa.analyze(c)

                #print(c , state)
                
                #if this is a comment check for new line so we can add to token stream
                if state == 6:
                    
                    
                    if (pos + 1) < max_pos and code[pos] == '\\' and code[pos + 1] == 'n':
                        pos += 2
                        self.dfa.reset()
                        self.token_stream.append(t.Token.COMMENT.name)

                #if this is a space not in a comment    
                elif state == 31:
                    last_success_state = self.dfa.get_last_success_state()

                    #if there was a success state before this space
                    if last_success_state != 0:
                        self.token_stream.append(self.dfa.get_token(last_success_state))
                    
                    self.dfa.reset()
                    
                #if this is a special character not in the dfa
                elif state == 30:

                    last_success_state = self.dfa.get_last_success_state()
                    self.dfa.reset()
                    #if there was a success state before this special character
                    #mainly for identifier  preceding increment or decrement
                    if last_success_state != 0:
                        self.token_stream.append(self.dfa.get_token(last_success_state))

                    match c:
                        case '(':
                            self.token_stream.append(t.Token.LEFT_PAREN.name)
                        case ')':
                            self.token_stream.append(t.Token.RIGHT_PAREN.name)
                        case '[':
                            self.token_stream.append(t.Token.LEFT_BRACKET.name)
                        case ']':
                            self.token_stream.append(t.Token.RIGHT_BRACKET.name)
                        case '{':
                            self.token_stream.append(t.Token.LEFT_BRACE.name)
                        case '}':
                            self.token_stream.append(t.Token.RIGHT_BRACE.name)
                        case '.':
                            self.token_stream.append(t.Token.DOT.name)
                        case '+':
                            if pos != max_pos and code[pos] == '+':
                                self.token_stream.append(t.Token.INCREMENT.name)
                                pos += 1
                            else:
                                self.token_stream.append(t.Token.PLUS.name)
                        case '-':
                            if pos != max_pos and code[pos] == '-':

                                self.token_stream.append(t.Token.DECREMENT.name)
                                pos += 1
                            else:
                                self.token_stream.append(t.Token.MINUS.name)
                        case '*':
                            self.token_stream.append(t.Token.MULTIPLY.name)
                        case '/':
                            self.token_stream.append(t.Token.DIVIDE.name)
                        case '%':
                            self.token_stream.append(t.Token.MODULUS.name)
                        case '<':
                            if pos != max_pos and code[pos] == '=':
                                self.token_stream.append(t.Token.LESS_THAN_EQ.name)
                                pos += 1
                            else:    
                                self.token_stream.append(t.Token.LESS_THAN.name)
                        case '>':
                            if pos != max_pos and code[pos] == '=':
                                self.token_stream.append(t.Token.GREATER_THAN_EQ.name)
                                pos += 1
                            else:
                                self.token_stream.append(t.Token.GREATER_THAN.name)
                        case '=':
                            if pos != max_pos and code[pos] == '=':
                                self.token_stream.append(t.Token.LOGIC_EQUAL.name)
                                pos += 1
                            else:
                                self.token_stream.append(t.Token.ASSIGNMENT.name)
                        case ';':
                            self.token_stream.append(t.Token.SEMICOLON.name)
                        case ',':
                            self.token_stream.append(t.Token.COMMA.name)
                        case '!':
                            self.token_stream.append(t.Token.LOGIC_NOT.name)
                        case '&':
                            if pos != max_pos and code[pos] == '&':
                                self.token_stream.append(t.Token.LOGIC_AND.name)
                                pos += 1
                            else:
                                self.token_stream.append(t.Token.BIT_AND.name)
                        case '|':
                            if pos != max_pos and code[pos] == '|':
                                self.token_stream.append(t.Token.LOGIC_OR.name)
                                pos += 1
                            else:
                                self.token_stream.append(t.Token.BIT_OR.name)
                        case '\\':
                            if pos != max_pos and code[pos] == 'n':
                                pos += 1
                        case _:
                            pass
        
    
    def reset(self):
        self.dfa.reset()
        self.token_stream = []
    
    def get_token_stream(self):
        return self.token_stream
    
    def get_keywords(self):
        return self.keywords
        



