class Monoalphabetic:
    def __init__(self, selection):
        self.selection = selection
        self.plaintext = ''
        self.ciphertext = ''
        self.key = ''

        # Runs the scheme
        self.get_vars()
        if selection == 'Enc':
            encrypted = self.enc()
            print('Ciphertext:', ''.join(map(str, encrypted)), '\n')
        elif selection == 'Dec':
            decrypted = self.dec()
            print('Plaintext:', ''.join(map(str, decrypted)), '\n')

    # Gets the variables from the user
    def get_vars(self):
        # Gets and validates value for key
        while True:
            print('\nPlease enter your key as a line of letters below...')
            print('Ex: qwertyuiopasdfghjklzxcvbnm means a -> q, b -> w, etc.')
            self.key = input('Key: ')

            # Strips whitespace
            self.key = ''.join(self.key.split())

            # If key is in letter format
            if self.key.isalpha():
                # Forces lowercase
                self.key = self.key.lower()

                # Checks key length
                if len(self.key) != 26:
                    print('Key length must be full 26 letters.')
                    continue

                # Checks for duplicate letters
                if not len(set(self.key)) == len(self.key):
                    print('Letters may only be used once.')
                    continue
                break
            else:
                print('Please only enter keys as letters. Refer to example.')
                continue

        # Gets and validates the plaintext
        while True:
            txt = input('Please enter your message: ')

            # Strips whitespace and forces lowercase
            txt = ''.join(txt.split())
            txt = txt.lower()

            # Checks for any other invalid characters
            if not txt.isalpha():
                print('Message must only be letters')
                continue
            break

        # Sets the message to the appropriate variable
        if self.selection == 'Enc':
            self.plaintext = txt
        elif self.selection == 'Dec':
            self.ciphertext = txt

    def enc(self):
        # Loops through letters and matches them to key
        for char in self.plaintext:
            pos = ord(char) - ord('a')
            self.ciphertext += self.key[pos]
        return self.ciphertext

    def dec(self):
        # Loops through letters and matches them to key
        for char in self.ciphertext:
            pos = self.key.index(char)
            self.plaintext += chr(pos + ord('a'))
        return self.plaintext


"""
# Test case:
test1 = Monoalphabetic('Enc')
test1.get_vars()
result = test1.enc()
print(result)

# Message: thisisatestofthesystem
# Key: qwertyuiopasdfghjklzxcvbnm
if result == 'ziololqztlzgyzitlnlztd':
    print('PASSED')
else:
    print('!!!FAILED!!!')

test2 = Monoalphabetic('Dec')
test2.get_vars()
result2 = test2.dec()
print(result2)

# Message: ziololqztlzgyzitlnlztd
# Key: qwertyuiopasdfghjklzxcvbnm
if result2 == 'thisisatestofthesystem':
    print('PASSED')
else:
    print('!!!FAILED!!!')
"""
