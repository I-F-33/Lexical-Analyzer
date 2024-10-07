from tokens.token_type import Token_type
from tokens.token import Token 
from dfa import DFA

class LexicalAnalyzer:

    def __init__(self):
        self.dfa = DFA()
        self.keywords = [
        'int', 'float', 'char', 'main', 'return', 'while', 'for', 'break',
        'if', 'else', 'goto', 'continue', 'switch', 'case', 'unsigned', 'void', 'do'
        ]
        self.token_stream = []


    def lex(self, filename):

        with open(filename, 'r') as file:
            code = file.read()
            code = code.replace("\n", "\\n")

            
            pos = 0
            max_pos = len(code)

            #if capturing a character sequence then turn on
            capture_flag = False

            #start of captured character sequence
            identifier_start = 0

            #line in code
            line = 1

            #while there are still characters to read
            while pos < max_pos:
                
                c = code[pos]
                

                state = self.dfa.analyze(c)

                #if we are in the number or identifier branch
                #then set the capture flag and mark the position as the start of the identifier
                if state == 3 or state == 4:
                    if not capture_flag:
                        identifier_start = pos
                        capture_flag = True


                pos += 1
                
                #if we are in the comment branch then check to see if we encountered a newline 
                if state == 6:
                    
                    #if theres a new line break then add comment token to token stream
                    if (pos + 1) < max_pos and code[pos] == '\\' and code[pos + 1] == 'n':
                        pos += 2
                        self.dfa.reset()
                        self.token_stream.append(Token(Token_type.COMMENT.name))
                        line += 1

                #if this is a space not in a comment    
                elif state == 31:
                    last_success_state = self.dfa.get_last_success_state()

                    #if there was a success state before this space
                    #then add its respective token to the token stream 
                    if last_success_state != 0:
                        
                        identifier = code[identifier_start:pos-1]
                        self._add_success_token(last_success_state, identifier)
                        identifier_start = 0
                        capture_flag = False

                    self.dfa.reset()
                    
                #if this is a special character not in the dfa
                elif state == 30:

                    last_success_state = self.dfa.get_last_success_state()
                    self.dfa.reset()

                    #if there was a success state before this special character
                    #then add its respective toke into the token stream
                    if last_success_state != 0:

                        identifier = code[identifier_start:pos-1]
                        self._add_success_token(last_success_state, identifier)
                        identifier_start = 0
                        capture_flag = False
                    
                    #match the character with its appropriate token
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
                            if pos < max_pos and code[pos] == '=':
                                self.token_stream.append(Token(Token_type.LOGICAL_NOT_EQUAL))
                                pos += 1
                            else:
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
    
    def _add_success_token(self, success_state, identifier):
        '''
        this function takes in a success state and a combination of characters successfully recognized as an identifier
        if the identifier is in [int,float,char,void] then add a basic token
        else add a regular identifier token

        if its a number then add a number token

        if its a division character then add divide token
        '''

        if success_state == 3 or success_state == 9 or success_state == 10:
            match identifier:
                case 'float' | 'int' | 'char' | 'void':
                     self.token_stream.append(Token(Token_type.BASIC.name, identifier ))
                case 'if':
                    self.token_stream.append(Token(Token_type.IF.name, identifier ))
                case 'else':
                    self.token_stream.append(Token(Token_type.ELSE.name, identifier ))
                case 'while':
                    self.token_stream.append(Token(Token_type.WHILE.name, identifier ))
                case 'main':
                    self.token_stream.append(Token(Token_type.MAIN.name, identifier ))
                case 'break':
                    self.token_stream.append(Token(Token_type.BREAK.name, identifier ))
                case 'do':
                    self.token_stream.append(Token(Token_type.DO.name, identifier ))

        elif success_state == 4:
            self.token_stream.append(Token(Token_type.NUMBER.name, identifier))
        elif success_state == 12:
            self.token_stream.append(Token(Token_type.REAL.name, identifier))
        elif success_state == 2:
            self.token_stream.append(Token(Token_type.DIVIDE.name))
        
