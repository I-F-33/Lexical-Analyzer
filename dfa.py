class DFA:

    def __init__(self):
        self.start_state = 1
        self.state = self.start_state
        self.accept_states = {3,4,8,9,10}
        self.prev_char = None

    def dfa(self, char):
        ascii_value = ord(char)

        #Start state
        if self.state == 1:
            if char == '/':
                self.state = 2
            elif char.isalpha():
                self.state = 3
            elif char.isdigit():
                self.state = 4
        #Comment branch
        elif self.state == 2:
            if char == '/':
                self.state = 5
        elif self.state == 5:
            if 32 <= ascii_value <= 126:
                self.prev_char = char
                self.state = 6
            
        #identifier branch
        elif self.state == 3:
            if char.isalpha():
                self.state = 9
            elif char.isdigit():
                self.state = 10
        elif 


    
