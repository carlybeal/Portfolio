class Caesar:
    def __init__(self, selection):
        self.selection = selection
        self.plaintext = ''
        self.ciphertext = ''
        self.shift = 0

        self.get_message()
        self.get_shift()

        if selection == 'Enc':
            encrypted = self.encrypt()
            print('Ciphertext:', ''.join(map(str, encrypted)), '\n')

        elif selection == 'Dec':
            decrypted = self.decrypt()
            print('Plaintext:', ''.join(map(str, decrypted)), '\n')

    def get_message(self):
        txt = 0
        flag = 0
        while flag == 0:  # Get and validate inputs
            txt = input('Please enter the message: ')
            txt = txt.replace(' ', '')
            txt = txt.upper()
            if not txt.isalpha():
                print('Please enter only letters')
            else:
                if self.selection == 'Enc':
                    self.plaintext = txt
                elif self.selection == 'Dec':
                    self.ciphertext = txt
                flag = 1

    def get_shift(self):
        flag = 0
        while flag == 0:  # Get and shift input
            self.shift = input('Please enter the shift: ')
            if not self.shift.isnumeric():
                print('Please enter a valid shift: numbers 1-25')
            elif not 1 <= int(self.shift) <= 25:
                print('Please enter a valid shift: numbers 1-25')
            else:
                self.shift = int(self.shift)
                flag = 1

    def encrypt(self):
        for i in range(len(self.plaintext)):
            char = self.plaintext[i]
            self.ciphertext += chr((ord(char) + self.shift - 65) % 26 + 65)
        return self.ciphertext

    def decrypt(self):
        for i in range(len(self.ciphertext)):
            char = self.ciphertext[i]
            self.plaintext += chr((ord(char) - self.shift - 65) % 26 + 65)
        return self.plaintext
