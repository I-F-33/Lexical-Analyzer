class DFA:

    def __init__(self):
        self.start_state = 1
        self.state = self.start_state
        self.accept_states = {3,4,7,8,9}

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
                self.state = 6
            elif char == '\n':
                self.state = 7
        elif self.state == 6:
            if 32 <= ascii_value <= 126:
                self.state = 6
            elif char == '\n':
                self.state = 7


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
        

        



    
