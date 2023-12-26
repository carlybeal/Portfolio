import re


class Vigenere:
    def __init__(self, selection):
        self.selection = selection
        self.plaintext = ''
        self.ciphertext = ''
        self.key = []

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
            self.key = input('Please enter a key: ')

            # Regex to check if key is tuple:
            tuple_check = re.match(r'^\(\d+(,\s*\d+)*\)$', self.key)

            # Handles formatting the tuple
            if tuple_check is not None:
                # Strips and splits the string
                self.key = self.key.strip('()')
                elements = self.key.split(',')

                # Converts elements from stings to ints
                for i in range(len(elements)):
                    # Removes any leading or ending whitespace
                    elements[i] = elements[i].strip()
                    if elements[i].isdigit():
                        elements[i] = int(elements[i])
                self.key = tuple(elements)

            # If key is in letter format
            elif not self.key.isnumeric():
                # Strips any whitespace away + forces lowercase
                self.key = ''.join(self.key.split())
                self.key = self.key.lower()

                # Checks for punctuation or other invalid characters
                if not self.key.isalpha():
                    print('Please only enter keys as letters or tuples.')
                    print('Examples: (3, 10, 13) or dkn')
                    continue

                # Loops through to convert characters to numbers
                new_key = []
                for i, char in enumerate(self.key):
                    new_key += [ord(char) - ord('a')]
                self.key = tuple(new_key)
            else:
                print('Please only enter keys as letters or tuples.')
                print('Examples: (3, 10, 13) or dkn')
                continue
            break

        # Validates the plaintext
        while True:
            txt = input('Please enter your message: ')

            # Strips any whitespace away + forces lowercase
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
        # Enumerates through plaintext and calculates new cipher letter
        for i, char in enumerate(self.plaintext):
            # Gets shift value from key
            k = self.key[i % len(self.key)]

            # Gets ASCII number value for new letter
            new_letnum = (ord(char) - ord('a') + k) % 26

            # Adds letter to ciphertext
            self.ciphertext += chr(new_letnum + ord('a'))

        # Returns new ciphertext string
        return self.ciphertext

    # Calculates key based on ciphertext and plaintext
    def find_key(self):
        # Checks that plaintext and ciphertext are the same length
        if len(self.plaintext) != len(self.ciphertext):
            raise ValueError('Plaintext and ciphertext must be same length')

        # Loops through the messages
        for i, char in enumerate(self.plaintext):
            # Subtracts ciphertext letter from plaintext letter
            key_val = ord(self.ciphertext[i]) - ord(char)

            # Deals with negative numbers
            if key_val < 0:
                key_val = key_val + 26

            # Adds key value to key array
            self.key += [key_val]
        return tuple(self.key)

    def dec(self):
        # Enumerates through plaintext and calculates new cipher letter
        for i, char in enumerate(self.ciphertext):
            # Gets shift value from key
            k = self.key[i % len(self.key)]

            # Gets ASCII number value for new letter
            new_letnum = (ord(char) - ord('a') - k) % 26

            # Adds letter to plaintext
            self.plaintext += chr(new_letnum + ord('a'))

        return self.plaintext


# Test Cases:
"""
test1 = Vigenere('Enc')
test1.get_vars()
result = test1.enc()
print(result)

# Message: Thisisatestofthesystem
# Keys: (3, 10, 13) or dkn
if result == 'wrvvsfddrvdbiduhclvdrp':
    print('PASSED')
else:
    print('!!FAIL!!')

test2 = Vigenere('Dec')
test2.get_vars()
result2 = test2.dec()
print(result2)

# Message: wrvvsfddrvdbiduhclvdrp
# Keys: (3, 10, 13) or dkn
if result2 == 'thisisatestofthesystem':
    print('PASSED')
else:
    print('!!FAIL!!')
"""
