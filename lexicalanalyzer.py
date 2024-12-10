from tokens.token import *
from dfa import DFA
from symbol.symboltable import *

class LexicalAnalyzer:

    def __init__(self):
        self.dfa = DFA()
        self.keywords = [
        'int', 'float', 'char', 'main', 'return', 'while', 'for', 'break',
        'if', 'else', 'goto', 'continue', 'switch', 'case', 'unsigned', 'void', 'do'
        ]
        self.token_stream = []
        self.SymbolTable = SymbolTable()



    def lex(self, filename):

        with open(filename, 'r') as file:
            code = file.read()
            code = code.replace("\n", "\\n")

            #position of character in program stream
            pos = 0

            #position of character in line, will reset on every line break
            #necessary for error messges
            line_pos = 0
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
                line_pos += 1
                
                #if we are in the comment branch then check to see if we encountered a newline 
                if state == 6:
                    
                    #if theres a new line break then add comment token to token stream
                    if (pos + 1) < max_pos and code[pos] == '\\' and code[pos + 1] == 'n':
                        pos += 2
                        self.dfa.reset()
                        self.token_stream.append(Comment())
                        line += 1
                        line_pos = 0

                #if this is a space not in a comment    
                elif state == 31:
                    last_success_state = self.dfa.get_last_success_state()

                    #if there was a success state before this space
                    #then add its respective token to the token stream 
                    if last_success_state != 0:
                        
                        identifier = code[identifier_start:pos-1]
                        self._add_success_token(last_success_state, identifier, line, line_pos)
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
                        self._add_success_token(last_success_state, identifier, line, line_pos)
                        identifier_start = 0
                        capture_flag = False
                    
                    #match the character with its appropriate token
                    match c:
                        case '(':
                            token = Left_paren()
                            self.token_stream.append(token)

                        case ')':
                            token = Right_paren()
                            self.token_stream.append(token)

                        case '[':
                            token = Left_bracket()
                            self.token_stream.append(token)

                        case ']':
                            token = Right_bracket()
                            self.token_stream.append(token)

                        case '{':
                            token = Left_brace()
                            self.token_stream.append(token)

                        case '}':
                            token = Right_brace()
                            self.token_stream.append(token)

                        case '.':
                            token = Dot()
                            self.token_stream.append(token)

                        case '+':
                            #if we have an increment token then add it to the token stream and increment the position
                            if pos < max_pos and code[pos] == '+':
                                c+= code[pos]
                                token = Increment()
                                self.token_stream.append(token)

                                pos += 1
                            else:#otherwise its a plus token
                                token = Plus()
                                self.token_stream.append(token)

                        case '-':
                            #if we have a decrement token then add it to the token stream and increment the position
                            if pos < max_pos and code[pos] == '-':
                                c+= code[pos]
                                token = Decrement()
                                self.token_stream.append(token)

                                pos += 1
                            else:#otherwise its a minus token
                                token = Minus()
                                self.token_stream.append(token)

                        case '*':
                            token = Multiply()
                            self.token_stream.append(token)

                        case '/':
                            token = Divide()
                            self.token_stream.append(token)

                        case '%':
                            token = Modulus()
                            self.token_stream.append(token)

                        case '<':
                            #if we have a less than or equal token then add it to the token stream and increment the position
                            if pos < max_pos and code[pos] == '=':
                                c+= code[pos]
                                token = Less_than_eq()
                                self.token_stream.append(token)

                                pos += 1
                            else:#otherwise its a less than token
                                token = Less_than()
                                self.token_stream.append(token)

                        case '>':
                            #if we have a greater than or equal token then add it to the token stream and increment the position
                            if pos < max_pos and code[pos] == '=':
                                c+= code[pos]
                                token = Greater_than_eq()
                                self.token_stream.append(token)

                                pos += 1
                            else:#otherwise its a greater than token
                                token = Greater_than()
                                self.token_stream.append(token)

                        case '=':
                            #if we have an equal token then add it to the token stream and increment the position
                            if pos < max_pos and code[pos] == '=':
                                c+= code[pos]
                                token = Logic_equal()
                                self.token_stream.append(token)

                                pos += 1
                            else:#otherwise its an assignment token
                                token = Assignment()
                                self.token_stream.append(token)

                        case ';':
                            token = Semicolon()
                            self.token_stream.append(token)

                        case ',':
                            token = Comma()
                            self.token_stream.append(token)

                        case '!':
                            #if we have a not equal token then add it to the token stream and increment the position
                            if pos < max_pos and code[pos] == '=':
                                c+= code[pos]
                                token = Logical_not_equal()
                                self.token_stream.append(token)

                                pos += 1
                            else: #otherwise its a logical not
                                token = Logic_not()
                                self.token_stream.append(token)

                        case '&':
                            #if we have a double ampersand then its a logical and
                            if pos < max_pos and code[pos] == '&':
                                c+= code[pos]
                                token = Logic_and()
                                self.token_stream.append(token)

                                pos += 1
                            else:#otherwise its a bit and
                                token = Bit_and()
                                self.token_stream.append(token)
   
                        case '|':
                            #if we have a double pipe then add a logic or token
                            if pos < max_pos and code[pos] == '|':
                                c+= code[pos]
                                token = Logic_or()
                                self.token_stream.append(token)

                                pos += 1
                            else:
                                token = Bit_or()
                                self.token_stream.append(token)

                        case '\\':
                            if pos < max_pos and code[pos] == 'n':
                                pos += 1
                                #everytime we encounter a new line we increment the line number
                                line += 1
                                line_pos = 0
                        case _:
                            pass

                    # self.token_stream.append(token)
                    # symbol = Symbol(c, token.get_type(), line, line_pos, len(c))
                    # self.SymbolTable.add_symbol(symbol)
        

    def reset(self):
        self.dfa.reset()
        self.token_stream = []
    
    def get_token_stream(self):
        return self.token_stream
    
    def get_keywords(self):
        return self.keywords
    
    def _add_success_token(self, success_state, identifier, line, line_pos):
        '''
        this function takes in a success state and a combination of characters successfully recognized as an identifier
        if the identifier is a reserved keyword then add its apprpriate token to the token stream
        else add a regular identifier token

        if its a number then add a number token

        if its a decimal number then add a real token

        if its a division character then add divide token
        '''

        if success_state == 3 or success_state == 9 or success_state == 10:
            match identifier:
                case 'float' | 'int' | 'char' | 'void':
                    token = Basic(identifier)
                case 'if':
                    token = If()
                case 'else':
                    token = Else()
                case 'while':
                    token = While()
                case 'main':
                    token = Main()
                case 'break':
                    token = Break()
                case 'do':
                    token = Do()
                case 'return':
                    token = Return()
                case 'for':
                    token = For()
                case 'unsigned':
                    token = Unsigned()
                case 'goto':
                    token = Goto()
                case 'continue':
                    token = Continue()
                case 'switch':
                    token = Switch()
                case 'case':
                    token = Case()
                case _:
                    token = Identifier(identifier)
            
            self.token_stream.append(token)
            symbol = Symbol(identifier, token.get_type(), line, line_pos, len(identifier))
            self.SymbolTable.add_symbol(symbol)

        elif success_state == 4:
            token = Number(identifier)
            self.token_stream.append(token)
            

        elif success_state == 12:
            token = Real(identifier)
            self.token_stream.append(token)

        elif success_state == 2:
            token = Divide()
            self.token_stream.append(token)
        
    def print_symbol_table(self):
        self.SymbolTable.display()