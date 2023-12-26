import re
import numpy


class Hill:
    def __init__(self, selection):
        self.selection = selection
        self.plaintext = []
        self.ciphertext = []
        self.key = []
        self.inverse_key = []

        # Runs the scheme
        self.get_vars()
        if selection == 'Enc':
            encrypted = self.enc()
            print('Ciphertext:', ''.join(map(str, encrypted)), '\n')
        elif selection == 'Dec':
            decrypted = self.dec()
            print('Plaintext:', ''.join(map(str, decrypted)), '\n')


    def validate_key(self):
        # Gets and validates value for key
        while True:
            """
            # Gets the key matrix size (n x n)
            try:
                key_size = int(input('Size (n) of key matrix: '))
            except ValueError:
                print('Key size must be numeric.')
                continue

            # Tests that matrix size is in range
            if key_size < 2 or key_size > 9:
                print('Matrix size must be between 2 and 9 (inclusive)')
                continue
            """
            # Sets up the matrix for the key
            self.key = [[0 for row in range(3)] for col in range(3)]

            # Gets the key
            key_input = input('Please enter a key: ')

            # Regex to check if message is matrix:
            matrix_check = re.match(r'^\[\d+(,\s*\d+)*]$', key_input)

            # Handles formatting the matrix
            if matrix_check is not None:
                # Strips any whitespace and splits string
                key_input = key_input.strip('[]')
                elements = key_input.split(',')

                # Converts elements from char to int
                for i in range(len(elements)):
                    # Removes whitespace
                    elements[i] = elements[i].strip()
                    if elements[i].isdigit():
                        elements[i] = int(elements[i])
                    else:
                        print('If using matrix form please only enter numbers')
                        continue

                i = 0
                for row in range(len(self.key)):
                    for col in range(len(self.key)):
                        self.key[row][col] = elements[i]
                        i += 1

                # Checks that matrix is correct size
                if len(self.key) != 3 or len(self.key[0]) != 3:
                    print('Key must fit into a 3 x 3 matrix (9 letters)')
                    continue

            # If message is in letter format
            elif not key_input.isnumeric():
                # Strips any whitespace and forces lowercase
                key_input = ''.join(key_input.split())
                key_input = key_input.lower()

                # Checks for any other invalid characters
                if not key_input.isalpha():
                    print('Please only enter keys as letters or matrices.')
                    print('Examples: [3, 10, 13] or dkn')
                    continue

                # Checks key size is square
                if not len(key_input) == 9:
                    print('Key must fit 3 x 3 matrix.')
                    continue

                # Loops through to convert characters to numbers
                new_key = []
                for i, char in enumerate(key_input):
                    new_key += [ord(char) - ord('a')]

                i = 0
                for row in range(len(self.key)):
                    for col in range(len(self.key)):
                        self.key[row][col] = new_key[i]
                        i += 1
            else:
                print('Please only enter keys as letters or matrices.')
                print('Examples: [3, 10, 13] or dkn')
                continue
            break
        return

    # Gets the variables from the user
    def validate_message(self):
        # Validates the message
        while True:
            txt = input('Please enter your message: ')

            # Regex to check if message is matrix:
            matrix_check = re.match(r'^\[?\d+(,\s*\d+)*]$', txt)

            # Handles formatting the matrix
            if matrix_check is not None:
                # Strips any whitespace and splits string
                txt = txt.strip('[]')
                elements = txt.split(',')

                # Converts elements from char to int
                for i in range(len(elements)):
                    # Removes whitespace
                    elements[i] = elements[i].strip()
                    if elements[i].isdigit():
                        elements[i] = [int(elements[i])]
                    else:
                        print('If using matrix form please only enter numbers')
                        continue

                txt = list(elements)

            # If message is in letter format
            elif not txt.isnumeric():
                # Strips any whitespace and forces lowercase
                txt = ''.join(txt.split())
                txt = txt.lower()

                # Checks for any other invalid characters
                if not txt.isalpha():
                    print('Please only enter messages as letters or matrices.')
                    print('Examples: [3, 10, 13] or dkn')
                    continue

                # Loops through to convert characters to numbers
                new_matrix = []
                for i, char in enumerate(txt):
                    new_matrix += [[ord(char) - ord('a')]]
                txt = new_matrix
            else:
                print('Please only enter messages as letters or matrices.')
                print('Examples: [3, 10, 13] or dkn')
                continue
            break

        # Sets the message to the appropriate variable
        if self.selection == 'Enc':
            self.plaintext = txt
        elif self.selection == 'Dec':
            self.ciphertext = txt

        return

    def get_vars(self):
        print('Can take keys and messages is matrix or alphabetical form')
        print('NOTE: If entering in matrix form, enter in as 1D matrix')
        print()

        self.validate_key()
        self.validate_message()
        return

    def convert_message(self, og_mess, key, wanted_mess):
        # Evens plaintext to block size
        remainder = len(og_mess) % len(key)
        if remainder > 0:
            for i in range(len(key) - remainder):
                # Adds X to end to even out blocks
                og_mess += [[ord('x') - ord('a')]]

        block_index = 0
        # Loops through the blocks
        for block in range(1, len(og_mess) // len(key) + 1):
            # (Re)sets current block
            cur_block = []
            for i in range(len(key)):
                cur_block += [og_mess[block_index]]
                block_index += 1

            cipher_block = [[0] for row in range(len(cur_block))]

            # Loops through and multiplies
            for row in range(len(key)):
                for elt in range(len(cur_block)):
                    cipher_block[row][0] += key[row][elt] * cur_block[elt][0]
                cipher_block[row][0] = cipher_block[row][0] % 26

            # Adds block to wanted message
            wanted_mess += cipher_block

        # Converts wanted_mess matrix to letter message
        message = ''
        for row in range(len(wanted_mess)):
            message += chr(wanted_mess[row][0] + ord('a'))

        return message

    def enc(self):
        return self.convert_message(self.plaintext, self.key, self.ciphertext)

    def inverse(self):
        det = int(numpy.linalg.det(self.key))
        det_multip_inverse = pow(det, -1, 26)
        self.inverse_key = [[0] * len(self.key) for i in range(len(self.key[0]))]
        for row in range(len(self.key)):
            for col in range(len(self.key[0])):
                dji = self.key
                dji = numpy.delete(dji, (col), axis=0)
                dji = numpy.delete(dji, (row), axis=1)
                det = dji[0][0] * dji[1][1] - dji[0][1] * dji[1][0]
                self.inverse_key[row][col] = (det_multip_inverse * pow(-1, row + col) * det) % 26
        return

    def dec(self):
        self.inverse()
        return self.convert_message(self.ciphertext, self.inverse_key, self.plaintext)


"""
# Test Cases:
# Message: 'actpoh' -> 'pohrvt'
# Key: 'GYBNQKURP' or [6, 24, 1, 13, 16, 10, 20, 17, 15]

test1 = Hill('Enc')
test1.get_vars()
result1 = test1.enc()
print(result1)
if result1 == 'pohrvt':
    print('PASSED')
else:
    print('!!!FAILED!!!')

test2 = Hill('Dec')
test2.get_vars()
result2 = test2.dec()
print(result2)
if result2 == 'act':
    print('PASSED')
else:
    print('!!!FAILED!!!')
"""
