import tokens 
class DFA:

    def __init__(self):
        self.start_state = 1
        self.state = self.start_state
        self.last_success_state = 0
        self.accept_states = {3,4,7,8,9}
        self.state_tokens = {
            3: tokens.Token.IDENTIFIER.name,
            4: tokens.Token.NUMBER.name,
            7: tokens.Token.COMMENT.name,
            8: tokens.Token.IDENTIFIER.name,
            9: tokens.Token.IDENTIFIER.name
        }
        

    def analyze(self, char):
        ascii_value = ord(char)

        
        #if SPACE AND NOT COMMENT THEN CODE IS 31
        if ascii_value == 32 and (self.state != 5 or self.state != 6):
            self.state = 31
        
        else:

            #Start state
            if self.state == 1:
                if char == '/':
                    self.state = 2
                elif char.isalpha():
                    self.last_success_state =  self.state = 3
                elif char.isdigit():
                    self.last_success_state =  self.state = 4

            #Comment branch
            elif self.state == 2:
                if char == '/':
                    self.state = 5
            elif self.state == 5:
                if 32 <= ascii_value <= 126:
                    self.state = 6
                elif char == '\n':
                    self.last_success_state = self.state = 7
            elif self.state == 6:
                if 32 <= ascii_value <= 126:
                    self.state = 6
                elif char == '\n':
                    self.last_success_state = self.state = 7


            #identifier branch
            elif self.state == 3:
                if char.isalpha():
                    self.state = 8
                elif char.isdigit():
                    self.state = 9

            elif self.state == 8:
                if char.isalpha():
                    self.state = 8
                elif char.isdigit():
                    self.state = 9
        
            elif self.state == 9:
                if char.isdigit():
                    self.state = 9
                elif char.isalpha():
                    self.state = 8

                

            #Number branch
            elif self.state == 4:
                if char.isdigit():
                    self.state = 4

            #default branch (special character and not comment)
            else:
                self.state = 30
            
            
        return self.state

    def reset(self):
        self.state = self.start_state


    def is_accept_state(self, state):
        return state in self.accept_states


    def get_token(self, state):
        
        temp = self.state_tokens[state]

        self.reset()

        self.last_success_state = self.start_state

        return temp

    
    def get_last_success_state(self):

        return self.last_success_state
    
