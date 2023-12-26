class SDES:
    # S-DES Constants
    P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    P8 = [6, 3, 7, 4, 8, 5, 10, 9]
    IP = [2, 6, 3, 1, 4, 8, 5, 7]
    IP_Inverse = [4, 1, 3, 5, 7, 2, 8, 6]
    EP = [4, 1, 2, 3, 2, 3, 4, 1]
    P4 = [2, 4, 3, 1]
    S0 = [[1, 0, 3, 2],
          [3, 2, 1, 0],
          [0, 2, 1, 3],
          [3, 1, 3, 2]]
    S1 = [[0, 1, 2, 3],
          [2, 0, 1, 3],
          [3, 0, 1, 0],
          [2, 1, 0, 3]]

    def __init__(self, selection):
        self.selection = selection
        self.plaintext = 0
        self.ciphertext = 0
        self.key = 0
        self.get_vars()

        if selection == 'Enc':
            encrypted = self.enc()
            print('Ciphertext:', ''.join(map(str, encrypted)), '\n')
            
        elif selection == 'Dec':
            decrypted = self.dec()
            print('Plaintext:', ''.join(map(str, decrypted)), '\n')

    def get_vars(self):
        flag = 0
        while flag == 0:  # Get and validate input for the key
            self.key = input('Please enter a 10-bit key: ')
            if not self.key.isnumeric():
                print('Key must be numerical')
            elif len(self.key) != 10:
                print('Key must be 10-bits')
            elif all(char in '01' for char in self.key):
                flag = 1
            else:
                print('Please enter only binary numbers')
        
        flag = 0  # Reinitialize flag to 0
        txt = 0
        while flag == 0:  # Get and validate input for the key
            txt = input('Please enter an 8-bit message: ')
            if not txt.isnumeric():
                print('Key must be numerical')
            elif len(txt) != 8:
                print('Message must be 8-bits')
            elif all(char in '01' for char in txt):
                break
            else:
                print('Please enter only binary numbers')
                continue
                
        if self.selection == 'Enc':
            self.plaintext = txt
        elif self.selection == 'Dec':
            self.ciphertext = txt

    def generate_subkeys(self, key):
        key = self.permute(key, self.P10)
        left, right = self.split_block(key)

        left = left[1:] + [left[0]]
        right = right[1:] + [right[0]]

        subkey1 = self.permute(left + right, self.P8)

        left = left[2:] + left[:2]
        right = right[2:] + right[:2]

        subkey2 = self.permute(left + right, self.P8)
        return subkey1, subkey2

    def initial_permutation(self, plain_text):
        return self.permute(plain_text, self.IP)

    def inverse_permutation(self, cipher_text):
        return self.permute(cipher_text, self.IP_Inverse)

    def permute(self, original, perm):
        return [original[i - 1] for i in perm]

    def split_block(self, block):
        mid = len(block) // 2
        left = block[:mid]
        right = block[mid:]
        return left, right

    def xor(self, left, right):
        return [l ^ r for l, r in zip(left, right)]

    def substitute(self, sub_block, s_box):
        row = int(sub_block[0] * 2 + sub_block[3])
        col = int(sub_block[1] * 2 + sub_block[2])
        return [int(bit) for bit in format(s_box[row][col], '02b')]

    def f_k(self, block, subkey):
        left, right = self.split_block(block)
        expanded_right = self.permute(right, self.EP)
        xored = self.xor(expanded_right, subkey)
        sub_block1 = xored[:4]
        sub_block2 = xored[4:]
        substituted1 = self.substitute(sub_block1, self.S0)
        substituted2 = self.substitute(sub_block2, self.S1)
        substituted = substituted1 + substituted2
        permuted = self.permute(substituted, self.P4)
        new_right = self.xor(left, permuted)
        return new_right + right

    def enc(self):
        self.key = [int(bit) for bit in self.key]
        self.plaintext = [int(bit) for bit in self.plaintext]
        subkey1, subkey2 = self.generate_subkeys(self.key)
        self.ciphertext = self.initial_permutation(self.plaintext)  # Permute plaintext with IP
        self.ciphertext = self.f_k(self.ciphertext, subkey1) 
        left, right = self.split_block(self.ciphertext)
        right, left = left, right                   # Switch
        self.ciphertext = left + right
        self.ciphertext = self.f_k(self.ciphertext, subkey2)
        self.ciphertext = self.inverse_permutation(self.ciphertext)
        return self.ciphertext

    def dec(self):
        self.key = [int(bit) for bit in self.key]
        self.ciphertext = [int(bit) for bit in self.ciphertext]
        subkey1, subkey2 = self.generate_subkeys(self.key)
        self.plaintext = self.initial_permutation(self.ciphertext)
        self.plaintext = self.f_k(self.plaintext, subkey2)
        left, right = self.split_block(self.plaintext)
        right, left = left, right
        self.plaintext = left + right
        self.plaintext = self.f_k(self.plaintext, subkey1)
        self.plaintext = self.inverse_permutation(self.plaintext)
        return self.plaintext
