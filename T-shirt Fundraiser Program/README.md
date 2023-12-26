# T-shirt Fundraiser Program

This program prompts the admin to enter their pin. The prompt is repeated until the correct pin is entered or there are 3 incorrect attempts where the program will quit.

Once the pin is entered correctly, the admin specifies how many organizations they would like to include. The admin will then enter the name, organization, shirt price, and percentage to go to the organization. The information is stored alphabetically in a linked list.

When prompted to enter t-shirt price, the prompt is repeated if not a valid input. The program will then prompt to verify the t-shirt price was entered correctly. When t-shirt price is verified, do the same for percentage to go to organization.

Once the organization name, t-shirt price, and percentage to go to organization is entered, the fundraisers are set up and the shirts can be sold.


Prompt the user to select the organization they want to purchase from. Then prompt the customer for t-shirt size. Repeat prompt if not a valid input. Prompt customer for shirt color. Repeat prompt if not a valid input. 

Once the customer has selected their size and color, prompt for their credit card in the following format ####-####-####-####. Validate the input and if not valid repeat the question. 

Once customer has inputted their credit card prompt, ask if they would like a receipt. If no is selected the program will go back to selling t-shirts. If yes is selected, the display order number (a random 4-digit number is created), shirt size, and color of shirt, percentage going to fundraiser and current amount raised for charity is printed to a file and then the program goes back to selling t-shirts.

Each receipt is appeneded to the file "receipt.txt"

To close the program, hit "q" in selling shirts, enter the admin pin. When pin is correct it will display the total sales and total amount raised for each organization. When the admin shuts down the system, the program will store the total sales and total funds raised for each organization.
