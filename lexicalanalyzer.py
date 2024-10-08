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
                        self.token_stream.append(Token(Token_type.COMMENT))
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
                            self.token_stream.append(Token(Token_type.LEFT_PAREN))
                        case ')':
                            self.token_stream.append(Token(Token_type.RIGHT_PAREN))
                        case '[':
                            self.token_stream.append(Token(Token_type.LEFT_BRACKET))
                        case ']':
                            self.token_stream.append(Token(Token_type.RIGHT_BRACKET))
                        case '{':
                            self.token_stream.append(Token(Token_type.LEFT_BRACE))
                        case '}':
                            self.token_stream.append(Token(Token_type.RIGHT_BRACE))
                        case '.':
                            self.token_stream.append(Token(Token_type.DOT))
                        case '+':
                            #if we have an increment token then add it to the token stream and increment the position
                            if pos < max_pos and code[pos] == '+':
                                self.token_stream.append(Token(Token_type.INCREMENT))
                                pos += 1
                            else:#otherwise its a plus token
                                self.token_stream.append(Token(Token_type.PLUS))
                        case '-':
                            #if we have a decrement token then add it to the token stream and increment the position
                            if pos < max_pos and code[pos] == '-':

                                self.token_stream.append(Token(Token_type.DECREMENT))
                                pos += 1
                            else:#otherwise its a minus token
                                self.token_stream.append(Token(Token_type.MINUS))
                        case '*':
                            self.token_stream.append(Token(Token_type.MULTIPLY))
                        case '/':
                            self.token_stream.append(Token(Token_type.DIVIDE))
                        case '%':
                            self.token_stream.append(Token(Token_type.MODULUS))
                        case '<':
                            #if we have a less than or equal token then add it to the token stream and increment the position
                            if pos < max_pos and code[pos] == '=':
                                self.token_stream.append(Token(Token_type.LESS_THAN_EQ))
                                pos += 1
                            else:#otherwise its a less than token
                                self.token_stream.append(Token(Token_type.LESS_THAN))
                        case '>':
                            #if we have a greater than or equal token then add it to the token stream and increment the position
                            if pos < max_pos and code[pos] == '=':
                                self.token_stream.append(Token(Token_type.GREATER_THAN_EQ))
                                pos += 1
                            else:#otherwise its a greater than token
                                self.token_stream.append(Token(Token_type.GREATER_THAN))
                        case '=':
                            #if we have an equal token then add it to the token stream and increment the position
                            if pos < max_pos and code[pos] == '=':
                                self.token_stream.append(Token(Token_type.LOGIC_EQUAL))
                                pos += 1
                            else:#otherwise its an assignment token
                                self.token_stream.append(Token(Token_type.ASSIGNMENT))
                        case ';':
                            self.token_stream.append(Token(Token_type.SEMICOLON))
                        case ',':
                            self.token_stream.append(Token(Token_type.COMMA))
                        case '!':
                            #if we have a not equal token then add it to the token stream and increment the position
                            if pos < max_pos and code[pos] == '=':
                                self.token_stream.append(Token(Token_type.LOGICAL_NOT_EQUAL))
                                pos += 1
                            else: #otherwise its a logical not
                                self.token_stream.append(Token(Token_type.LOGIC_NOT))
                        case '&':
                            #if we have a double ampersand then its a logical and
                            if pos < max_pos and code[pos] == '&':
                                self.token_stream.append(Token(Token_type.LOGIC_AND))
                                pos += 1
                            else:#otherwise its a bit and
                                self.token_stream.append(Token(Token_type.BIT_AND))
                        case '|':
                            #if we have a double pipe then add a logic or token
                            if pos < max_pos and code[pos] == '|':
                                self.token_stream.append(Token(Token_type.LOGIC_OR))
                                pos += 1
                            else:
                                self.token_stream.append(Token(Token_type.BIT_OR))
                        case '\\':
                            if pos < max_pos and code[pos] == 'n':
                                pos += 1
                                #everytime we encounter a new line we increment the line number
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

        if its a decimal number then add a real token

        if its a division character then add divide token
        '''

        if success_state == 3 or success_state == 9 or success_state == 10:
            match identifier:
                case 'float' | 'int' | 'char' | 'void':
                     self.token_stream.append(Token(Token_type.BASIC, identifier ))
                case 'if':
                    self.token_stream.append(Token(Token_type.IF, identifier ))
                case 'else':
                    self.token_stream.append(Token(Token_type.ELSE, identifier ))
                case 'while':
                    self.token_stream.append(Token(Token_type.WHILE, identifier ))
                case 'main':
                    self.token_stream.append(Token(Token_type.MAIN, identifier ))
                case 'break':
                    self.token_stream.append(Token(Token_type.BREAK, identifier ))
                case 'do':
                    self.token_stream.append(Token(Token_type.DO, identifier ))

        elif success_state == 4:
            self.token_stream.append(Token(Token_type.NUMBER, identifier))
        elif success_state == 12:
            self.token_stream.append(Token(Token_type.REAL, identifier))
        elif success_state == 2:
            self.token_stream.append(Token(Token_type.DIVIDE))
        
