class Menu:
    def __init__(self, question, options):
        self.question = question
        self.options = options

    def print_menu(self):
        for i in range(1, len(self.options) + 1):
            print(i, '. ', self.options[i - 1], sep='')

    def get_option(self):
        while True:
            print("Option: ", end='')

            # Validates response is integer
            response = input()
            if not response.isdigit():
                print('Please only enter the number corresponding to your choice')
                continue
            else:
                response = int(response)

            # Checks if integer is in range
            if response < 1 or response > len(self.options):
                print("Please enter a valid option")
                continue

            break

        # Sets to valid index
        response -= 1
        return self.options[response]
