from tokens.token import *
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
                        self.token_stream.append(Comment())
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
                            self.token_stream.append(Left_paren())
                        case ')':
                            self.token_stream.append(Right_paren())
                        case '[':
                            self.token_stream.append(Left_bracket())
                        case ']':
                            self.token_stream.append(Right_bracket())
                        case '{':
                            self.token_stream.append(Left_brace())
                        case '}':
                            self.token_stream.append(Right_brace())
                        case '.':
                            self.token_stream.append(Dot())
                        case '+':
                            #if we have an increment token then add it to the token stream and increment the position
                            if pos < max_pos and code[pos] == '+':
                                self.token_stream.append(Increment())
                                pos += 1
                            else:#otherwise its a plus token
                                self.token_stream.append(Plus())
                        case '-':
                            #if we have a decrement token then add it to the token stream and increment the position
                            if pos < max_pos and code[pos] == '-':

                                self.token_stream.append(Decrement())
                                pos += 1
                            else:#otherwise its a minus token
                                self.token_stream.append(Minus())
                        case '*':
                            self.token_stream.append(Multiply())
                        case '/':
                            self.token_stream.append(Divide())
                        case '%':
                            self.token_stream.append(Modulus())
                        case '<':
                            #if we have a less than or equal token then add it to the token stream and increment the position
                            if pos < max_pos and code[pos] == '=':
                                self.token_stream.append(Less_than_eq())
                                pos += 1
                            else:#otherwise its a less than token
                                self.token_stream.append(Less_than())
                        case '>':
                            #if we have a greater than or equal token then add it to the token stream and increment the position
                            if pos < max_pos and code[pos] == '=':
                                self.token_stream.append(Greater_than_eq())
                                pos += 1
                            else:#otherwise its a greater than token
                                self.token_stream.append(Greater_than())
                        case '=':
                            #if we have an equal token then add it to the token stream and increment the position
                            if pos < max_pos and code[pos] == '=':
                                self.token_stream.append(Logic_equal())
                                pos += 1
                            else:#otherwise its an assignment token
                                self.token_stream.append(Assignment())
                        case ';':
                            self.token_stream.append(Semicolon())
                        case ',':
                            self.token_stream.append(Comma())
                        case '!':
                            #if we have a not equal token then add it to the token stream and increment the position
                            if pos < max_pos and code[pos] == '=':
                                self.token_stream.append(Logical_not_equal())
                                pos += 1
                            else: #otherwise its a logical not
                                self.token_stream.append(Logic_not())
                        case '&':
                            #if we have a double ampersand then its a logical and
                            if pos < max_pos and code[pos] == '&':
                                self.token_stream.append(Logic_and())
                                pos += 1
                            else:#otherwise its a bit and
                                self.token_stream.append(Bit_and())
                        case '|':
                            #if we have a double pipe then add a logic or token
                            if pos < max_pos and code[pos] == '|':
                                self.token_stream.append(Logic_or())
                                pos += 1
                            else:
                                self.token_stream.append(Bit_or())
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
                     self.token_stream.append(Basic(identifier))
                case 'if':
                    self.token_stream.append(If())
                case 'else':
                    self.token_stream.append(Else())
                case 'while':
                    self.token_stream.append(While())
                case 'main':
                    self.token_stream.append(Main())
                case 'break':
                    self.token_stream.append(Break())
                case 'do':
                    self.token_stream.append(Do())
                case _:
                    self.token_stream.append(Identifier(identifier))

        elif success_state == 4:
            self.token_stream.append(Number(identifier))
        elif success_state == 12:
            self.token_stream.append(Real(identifier))
        elif success_state == 2:
            self.token_stream.append(Divide())
        
