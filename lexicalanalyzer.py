from tokens.token_type import Token_type
from tokens.token import Token 
from dfa import DFA

class LexicalAnalyzer:

    def __init__(self):
        self.dfa = DFA()
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

            
            capture_flag = False
            identifier_start = 0
            line = 1

            while pos < max_pos:
                
                c = code[pos]
                

                state = self.dfa.analyze(c)

                if state == 3 or state == 4:
                    if not capture_flag:
                        identifier_start = pos
                        capture_flag = True


                pos += 1
                #print(c , state)
                
                #if this is a comment check for new line so we can add to token stream
                if state == 6:
                    
                    
                    if (pos + 1) < max_pos and code[pos] == '\\' and code[pos + 1] == 'n':
                        pos += 2
                        self.dfa.reset()
                        self.token_stream.append(Token(Token_type.COMMENT.name))
                        line += 1

                #if this is a space not in a comment    
                elif state == 31:
                    last_success_state = self.dfa.get_last_success_state()

                    #if there was a success state before this space
                    if last_success_state != 0:
                        if last_success_state == 3 or last_success_state == 9 or last_success_state == 10:
                            self.token_stream.append(Token(Token_type.IDENTIFIER.name, code[identifier_start:pos-1]))
                            #print(code[identifier_start:pos-1])
                        elif last_success_state == 4:
                            self.token_stream.append(Token(Token_type.NUMBER.name, code[identifier_start:pos-1]))
                           # print(code[identifier_start:pos-1])
                        elif last_success_state == 2:
                            self.token_stream.append(Token(Token_type.DIVIDE.name))
                            #print(code[identifier_start:pos-1])
                        identifier_start = 0
                        capture_flag = False
                    self.dfa.reset()
                    
                #if this is a special character not in the dfa
                elif state == 30:

                    last_success_state = self.dfa.get_last_success_state()
                    self.dfa.reset()
                    #if there was a success state before this special character
                    #mainly for identifier  preceding increment or decrement
                    if last_success_state != 0:
                        if last_success_state == 3 or last_success_state == 9 or last_success_state == 10:
                            self.token_stream.append(Token(Token_type.IDENTIFIER.name, code[identifier_start:pos-1]))
                           # print(code[identifier_start:pos-1])
                        elif last_success_state == 4:
                            self.token_stream.append(Token(Token_type.NUMBER.name, code[identifier_start:pos-1]))
                            #print(code[identifier_start:pos-1])
                        elif last_success_state == 2:
                            self.token_stream.append(Token(Token_type.DIVIDE.name))
                            #print(code[identifier_start:pos-1])
                        identifier_start = 0
                        capture_flag = False
                    

                    match c:
                        case '(':
                            self.token_stream.append(Token(Token_type.LEFT_PAREN.name))
                        case ')':
                            self.token_stream.append(Token(Token_type.RIGHT_PAREN.name))
                        case '[':
                            self.token_stream.append(Token(Token_type.LEFT_BRACKET.name))
                        case ']':
                            self.token_stream.append(Token(Token_type.RIGHT_BRACKET.name))
                        case '{':
                            self.token_stream.append(Token(Token_type.LEFT_BRACE.name))
                        case '}':
                            self.token_stream.append(Token(Token_type.RIGHT_BRACE.name))
                        case '.':
                            self.token_stream.append(Token(Token_type.DOT.name))
                        case '+':
                            if pos < max_pos and code[pos] == '+':
                                self.token_stream.append(Token(Token_type.INCREMENT.name))
                                pos += 1
                            else:
                                self.token_stream.append(Token(Token_type.PLUS.name))
                        case '-':
                            if pos < max_pos and code[pos] == '-':

                                self.token_stream.append(Token(Token_type.DECREMENT.name))
                                pos += 1
                            else:
                                self.token_stream.append(Token(Token_type.MINUS.name))
                        case '*':
                            self.token_stream.append(Token(Token_type.MULTIPLY.name))
                        case '/':
                            self.token_stream.append(Token(Token_type.DIVIDE.name))
                        case '%':
                            self.token_stream.append(Token(Token_type.MODULUS.name))
                        case '<':
                            if pos < max_pos and code[pos] == '=':
                                self.token_stream.append(Token(Token_type.LESS_THAN_EQ.name))
                                pos += 1
                            else:    
                                self.token_stream.append(Token(Token_type.LESS_THAN.name))
                        case '>':
                            if pos < max_pos and code[pos] == '=':
                                self.token_stream.append(Token(Token_type.GREATER_THAN_EQ.name))
                                pos += 1
                            else:
                                self.token_stream.append(Token(Token_type.GREATER_THAN.name))
                        case '=':
                            if pos < max_pos and code[pos] == '=':
                                self.token_stream.append(Token(Token_type.LOGIC_EQUAL.name))
                                pos += 1
                            else:
                                self.token_stream.append(Token(Token_type.ASSIGNMENT.name))
                        case ';':
                            self.token_stream.append(Token(Token_type.SEMICOLON.name))
                        case ',':
                            self.token_stream.append(Token(Token_type.COMMA.name))
                        case '!':
                            self.token_stream.append(Token(Token_type.LOGIC_NOT.name))
                        case '&':
                            if pos < max_pos and code[pos] == '&':
                                self.token_stream.append(Token(Token_type.LOGIC_AND.name))
                                pos += 1
                            else:
                                self.token_stream.append(Token(Token_type.BIT_AND.name))
                        case '|':
                            if pos < max_pos and code[pos] == '|':
                                self.token_stream.append(Token(Token_type.LOGIC_OR.name))
                                pos += 1
                            else:
                                self.token_stream.append(Token(Token_type.BIT_OR.name))
                        case '\\':
                            if pos < max_pos and code[pos] == 'n':
                                pos += 1
                                line += 1
                        case _:
                            pass
        

    def reset(self):
        self.dfa.reset()
        self.token_stream = []
    
    def get_token_stream(self):
        return self.token_stream
    
    def get_keywords(self):
        return self.keywords
        