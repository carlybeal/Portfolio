class Playfair:
    def __init__(self, selection):
        self.selection = selection
        self.plaintext = 0
        self.ciphertext = 0
        self.key = 0
        self.plainTextList = 0
        self.final_matrix = 0

        self.get_key()
        self.final_matrix = self.get_final_matrix()

        if self.selection == 'Enc':
            self.encrypt()
        elif self.selection == 'Dec':
            self.decrypt()

    def get_key(self):
        flag = 0
        while flag == 0:  # Get and validate inputs
            self.key = input('Please enter the Key: ')
            self.key = self.key.replace(' ', '')
            self.key = self.key.upper()
            if not self.key.isalpha():
                print('Please enter only letters')
            else:
                flag = 1

    def validate_input(self):
        flag = 0
        txt = 0
        while flag == 0:  # Get and validate inputs
            txt = input('Please enter the message: ')
            txt = txt.replace(" ", "")
            txt = txt.upper()
            if not txt.isalpha():
                print('Please enter only letters')
            else:
                flag = 1
        return txt

    def initialize_matrix(self, x, y, initial):  # Initalizes the matrix and fills with 0
        return [[initial for i in range(x)] for j in range(y)]

    def get_final_matrix(self):
        k = 0  # for filling in the matrix
        flag = 0  # Variable for determining I/J
        result = list()
        for c in self.key:
            if c not in result:
                if c == 'J':
                    result.append('I')
                else:
                    result.append(c)

        for i in range(65, 91):
            if chr(i) not in result:
                if i == 73 and chr(74) not in result:  # 73 and 74 in ASCII is I and J
                    result.append('I')
                    flag = 1
                elif flag == 0 and i == 73 or i == 74:
                    pass
                else:
                    result.append(chr(i))

        self.final_matrix = self.initialize_matrix(5, 5, 0)  # Initialize matrix
        for i in range(0, 5):
            for j in range(0, 5):
                self.final_matrix[i][j] = result[k]
                k += 1
        return self.final_matrix

    def locindex(self, c):  # Get location of each character
        loc = list()
        if c == 'J':
            c = 'I'
        for i, j in enumerate(self.final_matrix):
            for k, l in enumerate(j):
                if c == l:
                    loc.append(i)
                    loc.append(k)
                    return loc

    def encrypt(self):  # Encryption
        self.plaintext = self.validate_input()  # Get the plaintext & validate input
        i = 0
        s = 0

        while s < len(self.plaintext) + 1:
            if s < len(self.plaintext) - 1:
                if self.plaintext[s] == self.plaintext[s + 1]:
                    self.plaintext = self.plaintext[:s + 1] + 'X' + self.plaintext[s + 1:]
                    s += 2
                else:
                    s += 2
            else:
                s += 1

        if len(self.plaintext) % 2 != 0:  # Add x to end of string if it's odd
            self.plaintext = self.plaintext[:] + 'X'

        print('Ciphertext:', end=' ')

        while i < len(self.plaintext):
            first_letter = list()
            first_letter = self.locindex(self.plaintext[i])
            sec_letter = list()
            sec_letter = self.locindex(self.plaintext[i + 1])
            if first_letter[1] == sec_letter[1]:
                print('{}{}'.format(self.final_matrix[(first_letter[0] + 1) % 5][first_letter[1]],
                                    self.final_matrix[(sec_letter[0] + 1) % 5][sec_letter[1]]), end='')
            elif first_letter[0] == sec_letter[0]:
                print('{}{}'.format(self.final_matrix[first_letter[0]][(first_letter[1] + 1) % 5],
                                    self.final_matrix[sec_letter[0]][(sec_letter[1] + 1) % 5]), end='')
            else:
                print('{}{}'.format(self.final_matrix[first_letter[0]][sec_letter[1]],
                                    self.final_matrix[sec_letter[0]][first_letter[1]]), end='')
            i = i + 2  # Move onto the next 2 letters
        print('\n')

    def decrypt(self):  # decryption
        self.ciphertext = self.validate_input()
        i = 0

        print('Plaintext:', end=' ')

        while i < len(self.ciphertext):
            first_letter = list()
            first_letter = self.locindex(self.ciphertext[i])
            sec_letter = list()
            sec_letter = self.locindex(self.ciphertext[i + 1])
            if first_letter[1] == sec_letter[1]:
                print('{}{}'.format(self.final_matrix[(first_letter[0] - 1) % 5][first_letter[1]],
                                    self.final_matrix[(sec_letter[0] - 1) % 5][sec_letter[1]]), end='')
            elif first_letter[0] == sec_letter[0]:
                print('{}{}'.format(self.final_matrix[first_letter[0]][(first_letter[1] - 1) % 5],
                                    self.final_matrix[sec_letter[0]][(sec_letter[1] - 1) % 5]), end='')
            else:
                print('{}{}'.format(self.final_matrix[first_letter[0]][sec_letter[1]],
                                    self.final_matrix[sec_letter[0]][first_letter[1]]), end='')
            i = i + 2
        print('\n')
