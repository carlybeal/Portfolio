from user_menu import Menu
from caesar import Caesar
from hill import Hill
from monoalphabetic import Monoalphabetic
from playfair import Playfair
from s_des import SDES
from vigenere import Vigenere

while True:
    # Handles the user menu
    q1 = Menu(print("Please choose an option:"), ("Enc", "Dec", "Exit"))
    q1.print_menu()
    enc_or_dec = q1.get_option()
    print("You chose:", enc_or_dec, '\n')

    if enc_or_dec == "Exit":
        break

    q2 = Menu(print("Which scheme would you like to use?"),
              ["Caesar", "Hill", "Monoalphabetic", "Playfair", "S-DES", "Vigenere"])
    q2.print_menu()
    scheme_choice = q2.get_option()
    print("You chose:", scheme_choice, '\n')

    if scheme_choice == "Caesar":
        Caesar(enc_or_dec)
    elif scheme_choice == "Hill":
        Hill(enc_or_dec)
    elif scheme_choice == "Monoalphabetic":
        Monoalphabetic(enc_or_dec)
    elif scheme_choice == "Playfair":
        Playfair(enc_or_dec)
    elif scheme_choice == "S-DES":
        SDES(enc_or_dec)
    elif scheme_choice == "Vigenere":
        Vigenere(enc_or_dec)
