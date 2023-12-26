# CS-4910 Final Project
### Carly Beal & Katie Schneider

This project includes 6 encryption schemes that the user can use. The user can pick whether to encrypt or decrypt a message using these schemes.

Caesar:
- The Caesar cipher is a shift cipher. To encode a message it takes in a key (an integer ranging from 0 - 25) and shifts the alphabet forward by that amount. So if the key was 3 and 'a' was entered in the message (plaintext) then the encoded message (ciphertext) would be 'd' because a -> b -> c -> d is 3 shifts forward. To decode the program takes the ciphertext and shifts the alphabet backward by that amount, so once again d -> c -> b -> a.
- The key only accepts integer values between 0 and 25 (inclusive) to be entered as input. It also restricts the message (plaintext and ciphertext) to being characters belonging to the alphabet. Spaces are ignored for the purposes of this implementation.

Hill:
- The Hill cipher relies on linear algebra concepts and blocking to encode messages. It converts messages into block sizes and puts those values into matrices. For this implementation, we used a block size of 3 so the resulting blocks are in matrices that are 3 x 1 in size. The key in this implementation is thus a 3 x 3 matrix. The Hill cipher uses matrix multiplication for encryption and decryption.
- On the encryption side it multiplies the key and the plaintext block together and mods it by 26 to get the resulting ciphertext block (also 3 x 1 in size). Then it combines all the blocks back together to get the resulting text. On the decryption side it multiples the inverse of the key (mod 26) and the ciphertext together, then modds by 26 again, to get the corresponding plaintext.
- This implementation allows the user to enter both the key and the messages as either 1D arrays or strings of letters. Only characters belonging to the alphabet are allowed in the character strings and spaces alongside case are ignored. Only integer values are allowed for the 1D array form of input. The program handles the conversion of these arrays and strings to a proper format for ease of use for the user.

Monoalphabetic:
- The monoalphabetic cipher is a substitution cipher. Letters map to each other on a one-to-one basis. For the key a user enters in a string that replaces the alphabet order so if you want a -> q, b -> w, c -> e, etc. you would use the key qwertyuiopasdfghjklzxcvbnm. q is in the 0 index of the string so it maps to a, w is in the 1 index of the string so it maps to b, and so forth.
- No letters can be repeated in the key string as the mapping of letters has to be 1 to 1 in order to be able to be decrypted. This cipher does not allow for any characters or numbers to be entered as input outside of the 26 letters of the alphabet (case independent). Spaces are ignored for the purposes of this implementation.

Playfair:
- The Playfair cipher operates on pairs of letters rather than individual letters. First, a 5x5 key table is generated that contains a keyword without repeating letters. The matrix is filled with the unique letters from the keyword, and any remaining letters of the alphabet are added in order (omitting the letter 'J' and usually combining 'I' and 'J'). If the plaintext message is odd, pad it with an extra letter to make it even. The plaintext is then divided into pairs of letters, for each pair, the following rules are applied to encrypt them:
  If both letters are in the same row, replace each letter with the letter to its right
  If both letters are in the same column, replace each letter with the letter below it
  If the letters are not in the same row or column, form a rectangle with these two
  letters and take the other two corners of the rectangle as the encrypted pair
To decrypt the message, use the same key matrix and apply the reverse process. Take pairs of letters from the ciphertext and use the same rules to find the original plaintext letters.
- Both the key and the message only take letters as inputs. It then removes all the spaces from the input and converts the input to all uppercase.

S-DES:
- The Simplified Data Encryption Standard (S-DES) uses a 10-bit key and the key is used to generate two 8-bit subkeys, K1 and K2. The 8-bit plaintext message is subjected to an initial permutation. The plaintext is then divided into two 4-bit blocks, L0 and R0. R0 is subjected to an expansion/permutation operation EP expanding it to 8 bits. The expanded R0 is XORed with the first subkey, K1. The result is passed through an S-box to obtain a 4-bit value. The output of the S-box is then subjected to permutation (P4) operation. The output of P4 is XORed with L0. The new R1 is the result of the XOR operation, and L1 is unchanged from L0. R1 and L1 from the previous round become R0 and L0 for the second round. The process is repeated to reach another P4. The final round outputs, R1 and L1, are swapped and the result is subjected to an inverse initial permutation to obtain the 8-bit ciphertext. Decryption follows the same steps but uses subkey K2 and K1 in reverse order. After the second round, the result is subjected to an inverse permutation to obtain the plaintext.
- Both the key and message only take in binary inputs.

Vigenere:
- The Vigenere cipher is also a form of shift cipher meant to more thoroughly hide letter frequencies. Like the Caesar cipher it shifts the alphabet forward by a specified amount for encryption and backward for decryption. However, in this encryption scheme, the key is a list of numbers (for this implementation stored in a tuple) that it cycles through to determine the shift amount for each letter of the plaintext or ciphertext. So a key of (3, 10, 13) here will shift the letters in groups of 3. The first letter of the group will be shifted forward 3 places in the alphabet (so 'a' -> 'd' like before). The second letter will be shifted by 10 places, and the 3rd letter of the group will be shifted by 13.
- This implementation allows for the key to be provided in either tuple/list form, examples: (3, 10, 13), (3), (5, 6, 7, 8, 9), or as a string of letters. So to represent a shift of (3, 10, 13) you could instead type 'dkn' for the key since 'd' is the 3rd letter of the alphabet (when you start with 'a' as 0), 'k' is the 10th letter, 'n' is the 13th letter. Messages (both plaintext and ciphertext) may only be characters belonging to the alphabet, spaces and case are ignored.
