//Carly Beal
// CS2060-002
/*this program is a t - shirt selling app.It starts with the admin pin to set up the program then customers can purchase t-shirts
until the admin closes the app for the day to get a summary of total sales and total funds raised for an organization */

#include <stdio.h>
#include <stdbool.h>
#include <math.h>
#include <ctype.h>
#include <stdlib.h>
#include <errno.h>
#include <time.h>
#include <float.h>
#include <string.h>

#define LENGTH 100 // For char const array
#define PIN 81405 // The PIN to get in
#define PERCENT_MIN 5 // Min percentage that can go towards fundraiser
#define PERCENT_MAX 20 // Max percentage that can go towards fundraiser
#define SHIRT_PRICE_MIN 20 // Min price
#define SHIRT_PRICE_MAX 50 // Max price
#define PIN_COUNTER 3 // Amount of times user can try the PIN before getting locked out
#define FILE_PATH "/Downloads" // File path to print to all documents to
#define RECEIPT_PATH "receipt.txt" // File to append receipts to
#define TOTAL_FUNDS_PATH "tshirtfund.txt" // File to print totals to
#define CREDIT_CARD_SIZE 19 // To check whole length inputted
#define DIGITS 4 // To check each section of token



typedef struct fundraiser {
	char organization[LENGTH];
	double shirtPrice;
	double fundPercent;
	double eachTotalSales;
	char terminate1[2];
	char terminate2[2];
	struct fundraiser* nextPtr;
} Fundraiser; // structure to store info

//declaring functions

//functions for linked list/structures
Fundraiser* insert(Fundraiser* headPtr, char* organization, double shirtPrice, double fundPercent); //function prototype for inserting data in alphabetical order
void display(Fundraiser* headPtr); // function to display linked list
bool access(char* organization, Fundraiser* headPtr, int numOrganizations); // Function to traverse and access each node


// original functions
int getAdminPin(); // admin pin should be whole number (81405). Function to set admin pin
double getShirtPrice(); // Function to set the price of the shirt.
double getFundPercent(); //function for setting percentage to go to fundraiser
char getShirtSize(); //function for shirtSize
char getShirtColor(); //function for shirtColor
void getCreditCard(char* organizationName, Fundraiser* headPtr); //function to get credit card
void getReceipt(char* organizationName, Fundraiser* headPtr, char shirtSize, char shirtColor, int numOrganizations); // function for generating receipt: size/color/shirt price/fundraiser percent/total sales
void grandTotal(char* organizationName, Fundraiser* headPtr, int numOrganizations); //calculates total sales and funds raised

//validation functions
bool getValidDouble(char* buff, double* const validDouble, int minVal, int maxVal); // Function to validate doubles (used for price and percent)
bool getValidInt(char* buff, int* const validInt); //function to validate int (used for credit card)
bool getValidChar(char* buff, char* const validChar); // function to validate shirtColor and shirtSize

int main() {
	Fundraiser* headPtr = NULL;
	Fundraiser* temp = (Fundraiser*)malloc(sizeof(Fundraiser));
	Fundraiser* previousPtr = NULL;
	bool isValid = false;
	bool stopSellingShirts = false; //to get out of customer interface
	char organizationName[LENGTH] = { "\0" }; // character array to store organization name
	char shirtSize = 'x', shirtColor = 'x';
	double shirtPrice = 0, fundPercent = 0;
	int numOrganizations = 0, length = 0;



	if (getAdminPin() == PIN) { //if login is successful
		puts("\n------ SHIRT FUNDRAISER SET UP ------\n");

		puts("How many organizations would you like to include?");
		scanf("%d", &numOrganizations);
		while ((getchar()) != '\n'); // clears buffer

		for (int counter = 0; counter < numOrganizations; counter++) {
			puts("\nEnter organization name:");
			scanf("%s", organizationName);
			while ((getchar()) != '\n'); // clears buffer

			shirtPrice = getShirtPrice(); // get the shirt price
			fundPercent = getFundPercent(); // get the fund percent
			headPtr = insert(headPtr, organizationName, shirtPrice, fundPercent); // put in linked list alphabetically
		}
		//end admin set up

		do {
			puts("\n\n\n\n\n------ T-SHIRT FUNDRAISER ------\n");

			puts("Organizations available to buy from:");
			display(headPtr);

			puts("\nWhich organization would you like to buy from?");
			scanf("%s", organizationName);
			while ((getchar()) != '\n'); // clears buffer


			length = strlen(organizationName);
			if (length == 1) {
				if ((strcmp(headPtr->terminate2, organizationName) == 0) || (strcmp(headPtr->terminate1, organizationName) == 0)) {
					if (getAdminPin() == PIN) {
						grandTotal(organizationName, headPtr, numOrganizations);
						return 0;
					}
					else {
						puts("Returning to vustomer interface");
					}
				}
			}

			else {
				isValid = access(organizationName, headPtr, numOrganizations); // checks if organization name is valid
				if (isValid) {
					shirtSize = getShirtSize(organizationName, headPtr, shirtPrice, fundPercent);
					shirtColor = getShirtColor();
					getCreditCard(organizationName, headPtr); // according to each organization

					temp = headPtr; // redeclare each time it loops
					int flag = 1; // redeclare each loop
					while (flag && temp != NULL) {
						if (strcmp(temp->organization, organizationName) == 0) { // if temp is an exact match to name of organization move on
							flag = 0;
						}
						else { //else it will go to next node and check again
							previousPtr = temp;
							temp = temp->nextPtr;
						}
					} // end of while statement
					if (temp == NULL) {
						puts("Uh Oh");
					}
					else {
						if (previousPtr == NULL) { // if first node is the node
							temp->eachTotalSales = temp->eachTotalSales + temp->shirtPrice; // adds up total Sales for first organization in linked list
							getReceipt(organizationName, headPtr, shirtSize, shirtColor, numOrganizations);
						}
						else { // node in between or end
							temp->eachTotalSales = temp->eachTotalSales + temp->shirtPrice; // adds up total sales for in between/end organizations in linked list
							getReceipt(organizationName, headPtr, shirtSize, shirtColor, numOrganizations);
						}
					}

				}
				else {
					printf("\n%s is not an available organization!\n\n", organizationName);
				}
			}
		} while (!stopSellingShirts);
	}
	else {
		free(temp);
		temp = NULL;
		puts("Exiting fundraiser app");
	}
	return 0;
} // end function main

//linked list functions

Fundraiser* insert(Fundraiser* headPtr, char* organizationName, double shirtPrice, double fundPercent) { //inserting data in alphabetical order

	Fundraiser* temp = (Fundraiser*)malloc(sizeof(Fundraiser));
	strcpy(temp->organization, organizationName);
	temp->shirtPrice = shirtPrice;
	temp->fundPercent = fundPercent;
	temp->eachTotalSales = 0;
	strcpy(temp->terminate1, "Q");
	strcpy(temp->terminate2, "q");


	if (headPtr == NULL) { //if list is empty add node
		temp->nextPtr = headPtr;
		headPtr = temp;
	}
	else { //else find postion after which new node will be added
		Fundraiser* temp1 = headPtr;
		Fundraiser* previousPtr = NULL;
		int flag = 1;
		while (flag && temp1 != NULL) { // temp1 will check a node is alphabetically greater
			if (strcmp(temp1->organization, organizationName) < 0) { // if it is, then move ahead, previousPtr will store node previousPtr of temp1
				previousPtr = temp1; // in case node found where it has to be added then previousPtr will need to
				temp1 = temp1->nextPtr; //adjust nodes.
			}
			else {
				flag = 0;
			}

		}
		if (previousPtr == NULL) {//if input name is highest in alphabet then it will be first node
			temp->nextPtr = headPtr;
			headPtr = temp;

		}
		else {// else it is in between list or at end.
			temp->nextPtr = previousPtr->nextPtr;
			previousPtr->nextPtr = temp;
		}
	}
	return headPtr;
}

void display(Fundraiser* headPtr) { // display list data
	while (headPtr != NULL) {
		printf("Name: %s\nShirt price: $%0.2f\nFund percent: %0.2f%%\n\n", headPtr->organization, headPtr->shirtPrice, headPtr->fundPercent);
		headPtr = headPtr->nextPtr;
	}

}

bool access(char* organizationName, Fundraiser* headPtr, int numOrganizations) { // access and display info for chosen fundraiser
	bool valid = false;
	Fundraiser* temp = (Fundraiser*)malloc(sizeof(Fundraiser));
	Fundraiser* previousPtr = NULL;
	temp = headPtr;
	int flag = 1;

	while (flag && temp != NULL) {
		if (strcmp(temp->organization, organizationName) == 0) { // if temp is an exact match to name of organization move on
			flag = 0;
		}
		else { //else it will go to next node and check again
			previousPtr = temp;
			temp = temp->nextPtr;
		}
	} // end of while statement

	if (temp == NULL) { // if nothing matching return false
		valid = false;
	}
	else {
		if (previousPtr == NULL) { // if first node is the node
			printf("\nBuy a shirt from %s and %0.2f%% will go to charity.\n", temp->organization, temp->fundPercent);
			printf("Shirt price is $%0.2f\n", temp->shirtPrice);
			valid = true;
		}
		else { // node in between or end
			printf("\nBuy a shirt from %s and %0.2f%% will go to charity.\n", temp->organization, temp->fundPercent);
			printf("Shirt price is $%0.2f\n", temp->shirtPrice);
			valid = true;
		}
	} // end else statement
	return valid;
} // end function traverse

//original functions

int getAdminPin() { //function for admin pin
	bool validInput = false;
	int adminPin = 0, counter = 0;
	int validScanInput = 0;

	for (counter = 1; counter <= PIN_COUNTER; counter++) {

		do {

			puts("Enter PIN: "); //prompts for pin
			validScanInput = scanf("%d", &adminPin); //stores input for validation
			while ((getchar()) != '\n'); // clears buffer


			if (validScanInput != 1) {
				puts("\nInvalid PIN entered");
				validInput = true;
			}
			else if (adminPin != PIN) { // if not 81405 then loop again 
				puts("\nInvalid PIN entered");
				validInput = true;
			}
			else {
				counter = PIN_COUNTER;
				validInput = true;
			}
		} while (validInput == false);
	}
	return adminPin;
} //end function getAdminPin 

double getShirtPrice() { //function for setting t-shirt price
	bool validInput = false;
	bool isValid = false;
	char charShirtPrice[10] = { "\0" };
	double shirtPrice = 0;
	char verify = 'x';
	//int inputLength = 0;

	do {

		do {

			puts("\nEnter the selling price of the t-shirt:");
			fgets(charShirtPrice, sizeof(charShirtPrice), stdin);//take in shirtPrice
			//inputLength = strlen(charShirtPrice);

			isValid = getValidDouble(charShirtPrice, &shirtPrice, SHIRT_PRICE_MIN, SHIRT_PRICE_MAX);
			if (isValid) {
				//printf("Integer value: %0.2f\n", doubleValue);
				validInput = true;
			}
			else {
				validInput = false;
			}
		} while (validInput == false); //makes this do-while loop repeat until an appropriate value is found

		printf("Is $%0.2f the correct price? \n", shirtPrice);

		do { // Yes or No

			validInput = false;

			puts("\nPlease enter (y)es or (n)o:");
			int validScanInput = scanf("%c", &verify);

			while ((getchar()) != '\n'); //clears the buffer

			if (validScanInput != 1) {
				puts("\nInvalid value entered. Enter y or n");
			}
			else if (tolower(verify) == 'n') {
				validInput = true;
			}
			else if (tolower(verify) == 'y') {
				validInput = true;
			}
			else {
				puts("\nInvalid value entered. Enter y or n");
			}
		} while (validInput == false); //loops until validInput becomes true

	} while (tolower(verify) == 'n');
	return shirtPrice;
}

double getFundPercent() { //function for setting up fundPercent
	bool validInput = false;
	bool isValid = false;
	char charFundPercent[10] = { "\0" };
	double fundPercent = 0;
	char verify = 'x';
	//int inputLength = 0;

	do {

		do {

			puts("\nEnter the fundraiser percentage of the t-shirt sales:");
			fgets(charFundPercent, sizeof(charFundPercent), stdin);

			isValid = getValidDouble(charFundPercent, &fundPercent, PERCENT_MIN, PERCENT_MAX);
			if (isValid) {
				validInput = true;
			}
			else {
				validInput = false;
			}
		} while (validInput == false); //makes this do-while loop repeat

		printf("Is %s%% the correct fundraiser percentage?\n", charFundPercent);

		do { // yes or no

			validInput = false;

			puts("\nPlease enter (y)es or (n)o:");
			int validScanInput = scanf("%c", &verify);

			while ((getchar()) != '\n'); //clears the buffer

			if (validScanInput != 1) {
				puts("\nInvalid value entered. Enter y or n");
			}
			else if (tolower(verify) == 'n') {
				validInput = true;
			}
			else if (tolower(verify) == 'y') {
				validInput = true;
			}
			else {
				puts("\nInvalid value entered. Enter y or n");
			}
		} while (validInput == false); //loops until validInput becomes true

	} while (tolower(verify) == 'n'); // if n then loop again for different percent

	return fundPercent;
}

char getShirtSize() {
	char validShirtSizes[LENGTH] = { 'S', 's', 'M', 'm', 'L', 'l', 'X', 'x', '\0' }; // array of characters
	char chooseShirtSize[10] = { "\0" };
	bool validInput = false;
	bool isValid = false;

	do {
		validInput = false;

		puts("\nEnter T-shirt size: (s)mall, (m)edium, (l)arge, or e(x)tra-large");
		fgets(chooseShirtSize, sizeof(chooseShirtSize), stdin);

		if (chooseShirtSize[strlen(chooseShirtSize) - 1] == '\n') {
			chooseShirtSize[strlen(chooseShirtSize) - 1] = '\0';
		}

		isValid = getValidChar(chooseShirtSize, validShirtSizes); // validates that the char inputted is one in the shirtSizeArray

		if (isValid) {
			validInput = true;
		}
		else {
			puts("Invalid size entered.");
		}
	} while (validInput == false);
	return toupper(chooseShirtSize[0]);
}

char getShirtColor() {
	char validShirtSizes[LENGTH] = { 'K', 'k', 'W', 'w', 'R', 'r', 'O', 'o', 'B', 'b', 'P', 'p', '\0' }; // array of characters
	char chooseShirtColor[10] = { "\0" };
	bool validInput = false;
	bool isValid = false;

	do {
		validInput = false;

		puts("\nEnter T-shirt color: blac(k), (w)hite, (r)ed, (o)range, (b)lue, (p)urple");
		fgets(chooseShirtColor, sizeof(chooseShirtColor), stdin);

		if (chooseShirtColor[strlen(chooseShirtColor) - 1] == '\n') {
			chooseShirtColor[strlen(chooseShirtColor) - 1] = '\0';
		}

		isValid = getValidChar(chooseShirtColor, validShirtSizes); // validates that the char inputted is one in the shirtSizeArray

		if (isValid) {
			validInput = true;
		}
		else {
			puts("Invalid color entered.");
		}
	} while (validInput == false);
	return toupper(chooseShirtColor[0]);
}

void getCreditCard(char* organizationName, Fundraiser* headPtr) {
	bool validCard = false;
	bool validNum = true;
	char creditCardNum[50] = { "" };
	const char delim[2] = "-";
	char* token;

	Fundraiser* temp = (Fundraiser*)malloc(sizeof(Fundraiser));
	Fundraiser* previousPtr = NULL;
	temp = headPtr;

	int flag = 1;

	while (flag && temp != NULL) {
		if (strcmp(temp->organization, organizationName) == 0) { // if temp is an exact match to name of organization move on
			flag = 0;
		}
		else { //else it will go to next node and check again
			previousPtr = temp;
			temp = temp->nextPtr;
		}
	} // end of while statement

	if (temp == NULL) { // if nothing matching return false
	}
	else {
		if (previousPtr == NULL) { // if first node is the node
			printf("\nYour cost is $%0.2f. Enter your credit card number in the format (####-####-####-####) to complete the payment:\n", temp->shirtPrice);
		}
		else {
			printf("\nYour cost is $%0.2f. Enter your credit card number in the format (####-####-####-####) to complete the payment:\n", temp->shirtPrice);
		}
	}

	do {

		validCard = false;
		//printf("\nYour cost is $%0.2f. Enter your credit card number in the format (####-####-####-####) to complete the payment:\n", headPtr->shirtPrice);
		fgets(creditCardNum, sizeof(creditCardNum), stdin); //take in shirtPrice

		if (creditCardNum[strlen(creditCardNum) - 1] == '\n') {
			creditCardNum[strlen(creditCardNum) - 1] = '\0';
		}

		size_t length = strlen(creditCardNum);
		if (length != CREDIT_CARD_SIZE) {
			puts("Invalid value entered");
		}
		else {
			validNum = true;
			token = strtok(creditCardNum, delim); //take the section before delim -

			if (token == NULL) {
				validNum = false;
				puts("Please enter a valid credit card number.");
			}
			else {
				while (token != NULL && validNum) {
					length = strlen(token);
					if (length != DIGITS) {
						validNum = false;
					}
					else {
						int cardNum = 0;
						validNum = getValidInt(token, &cardNum);
						//make a validInt function and pass
					}
					token = strtok(NULL, delim);
				}
			}
			if (!validNum) {
				puts("Please enter a valid credit card number.");
			}
			else {
				validCard = true;
			}
		}
	} while (validCard == false);
}

void getReceipt(char* organizationName, Fundraiser* headPtr, char shirtSize, char shirtColor, int numOrganizations) { //function to get receipt

	srand(time(NULL)); //randomize receipt number
	FILE* rfPtr;
	int receiptNum = 0;
	double currentFundsRaised = 0;
	bool validInput = false;
	int validScanInput = 0, flag = 1;
	char wantReceipt = 'x';

	Fundraiser* temp = (Fundraiser*)malloc(sizeof(Fundraiser));
	temp = headPtr;
	Fundraiser* previousPtr = NULL;

	do {
		validInput = false;

		puts("\nDo you want a receipt?");
		puts("Please enter (y)es or (n)o");
		validScanInput = scanf("%c", &wantReceipt);
		while ((getchar()) != '\n');

		if (validScanInput != 1) { //check if valid input
			puts("\nInvalid size entered.");
		}

		//continue on to shirt sizes
		//if did not want receipt then don't create file and continue to sell next shirt
		else if ((wantReceipt == 'N') || (wantReceipt == 'n')) { // if N/n then just print out to debug window
			while (flag && temp != NULL) {
				if (strcmp(temp->organization, organizationName) == 0) { // if temp is an exact match to name of organization move on
					flag = 0;
				}
				else { //else it will go to next node and check again
					previousPtr = temp;
					temp = temp->nextPtr;
				}
			} // end of while statement

			if (temp == NULL) { // if nothing matching return false
				validInput = false;
			}
			else {
				if (previousPtr == NULL) { // if first node is the node
					printf("\n%0.2f%% of your cost will be donated to charity", temp->fundPercent);
					puts("\nThank you for your support.\n\n");
					validInput = true;
				}
				else {
					printf("\n%0.2f%% of your cost will be donated to charity", temp->fundPercent);
					puts("\nThank you for your support.\n\n");
					validInput = true;
				}
			}
		}
		//if they did want a receipt open file and append all thats specificed
		else if ((wantReceipt == 'Y') || (wantReceipt == 'y')) { //if Y/y then have receipt print out to receipt.txt
			if ((rfPtr = fopen(FILE_PATH RECEIPT_PATH, "a+")) == NULL) { // if file can open then go to else
				puts("File could not be opened");
			}
			else {
				while (flag && temp != NULL) {
					if (strcmp(temp->organization, organizationName) == 0) { // if temp is an exact match to name of organization move on
						flag = 0;
					}
					else { //else it will go to next node and check again
						previousPtr = temp;
						temp = temp->nextPtr;
					}
				} // end of while statement

				if (temp == NULL) { // if nothing matching return false
					validInput = false;
				}
				else {
					if (previousPtr == NULL) { // if first node is the node
						receiptNum = (1000 + (rand() % 9000));
						fprintf(rfPtr, "Organization: %s\n", temp->organization); //tells which organization it was bought brom
						fprintf(rfPtr, "T-Shirt size: %c\n", shirtSize);		   // goes to file
						fprintf(rfPtr, "T-Shirt color: %c\n", shirtColor);		   // goes to file
						fprintf(rfPtr, "T-Shirt price: $%0.2f\n", temp->shirtPrice);	   // goes to file
						fprintf(rfPtr, "Receipt: #%d\n\n\n", receiptNum);	//goes to file

						printf("Organization: %s\n", temp->organization); // just prints out
						printf("T-Shirt size: %c\n", shirtSize);
						printf("T-Shirt color: %c\n", shirtColor);
						printf("T-Shirt price: $%0.2f\n", temp->shirtPrice);
						printf("Receipt: #%d\n\n\n", receiptNum);

						printf("\n%0.2f%% of your cost will be donated to charity", temp->fundPercent); // just prints out
						puts("\nThank you for your support.\n\n"); // just prints out
						validInput = true;
					}
					else { // for in between or end node
						receiptNum = (1000 + (rand() % 9000));
						fprintf(rfPtr, "Organization: %s\n", temp->organization); //tells which organization it was bought brom
						fprintf(rfPtr, "T-Shirt size: %c\n", shirtSize);		   // goes to file
						fprintf(rfPtr, "T-Shirt color: %c\n", shirtColor);		   // goes to file
						fprintf(rfPtr, "T-Shirt price: $%0.2f\n", temp->shirtPrice);	   // goes to file
						fprintf(rfPtr, "Receipt: #%d\n\n\n", receiptNum);	//goes to file

						printf("Organization: %s\n", temp->organization); // just prints out
						printf("T-Shirt size: %c\n", shirtSize);
						printf("T-Shirt color: %c\n", shirtColor);
						printf("T-Shirt price: $%0.2f\n", temp->shirtPrice);
						printf("Receipt: #%d\n\n\n", receiptNum);

						printf("\n%0.2f%% of your cost will be donated to charity", temp->fundPercent); // just prints out
						puts("\nThank you for your support.\n\n"); // just prints out

						validInput = true;
					}
				}
			}
			fclose(rfPtr);
		}
		else {
			puts("\nInvalid input entered");
			validInput = false;
		}

		while (headPtr != NULL) {
			currentFundsRaised = ((headPtr->eachTotalSales * headPtr->fundPercent) / 100) + currentFundsRaised;
			headPtr = headPtr->nextPtr;
		}
		printf("Current amount raised for charity is $%0.2f\n", currentFundsRaised); // just prints outs
	} while (validInput == false); // while its still false loop again

} //end of getReceipt function

void grandTotal(char* organizationName, Fundraiser* headPtr, int numOrganizations) {
	FILE* tfPtr;
	double totalSales = 0, fundsRaised = 0, overallTotalSales = 0, overallFundsRaised = 0;
	Fundraiser* temp = (Fundraiser*)malloc(sizeof(Fundraiser));
	temp = headPtr;


	if ((tfPtr = fopen(FILE_PATH TOTAL_FUNDS_PATH, "w")) == NULL) {
		puts("File could not be opened");
	}
	else {
		fprintf(tfPtr, "Totals for each organization:\n\n");
		puts("Totals for each organization:\n");
		while (headPtr != NULL) {
			totalSales = (headPtr->eachTotalSales);
			fundsRaised = ((headPtr->eachTotalSales * headPtr->fundPercent) / 100);

			fprintf(tfPtr, "Organization: %s\n", headPtr->organization);
			fprintf(tfPtr, "Total sales: $%0.2f\n", totalSales);
			fprintf(tfPtr, "Total amount raised: $%0.2f\n\n", fundsRaised);


			printf("\n\nOrganization: %s\n", headPtr->organization);
			printf("Total sales: $%0.2f\n", totalSales); // just prints outs
			printf("Total amount raised: $%0.2f\n", fundsRaised); // to see on screen

			headPtr = headPtr->nextPtr;
		}
		while (temp != NULL) {
			overallTotalSales = ((temp->eachTotalSales) + overallTotalSales);
			overallFundsRaised = ((temp->eachTotalSales * temp->fundPercent) / 100) + overallFundsRaised;
			temp = temp->nextPtr;
		}
		fprintf(tfPtr, "\n\nOverall total sales: $%0.2f\n", overallTotalSales); // to file
		fprintf(tfPtr, "Overall amount raised for charity is $%0.2f\n", overallFundsRaised);

		printf("\n\nOverall total sales: $%0.2f\n", overallTotalSales);
		printf("Overall amount raised for charity is $%0.2f\n", overallFundsRaised); // just prints o
		fclose(tfPtr);
	}
	puts("\nTotal sales and funds raised for each organization recorded\n");
}


//functions inside of functions
bool getValidDouble(char* buff, double* const validDouble, int minVal, int maxVal) { //function for validating double to go into shirtPrice/FundPercent	
	bool valid = false;
	char* endPtr;
	errno = 0;
	double doubleTest = 0;

	if (buff[strlen(buff) - 1] == '\n') {
		buff[strlen(buff) - 1] = '\0';
	}

	doubleTest = strtod(buff, &endPtr); // convert string to double and put in doubleTest, if theres anything other than numbers then put in endPtr

	if (endPtr == buff) {
		fprintf(stderr, "\n%s is not a decimal number.\n", buff);
	}
	else if ('\0' != *endPtr) {
		fprintf(stderr, "\n%s: extra characters at end of input: %s.\n", buff, endPtr);
	}
	else if ((DBL_MIN == doubleTest || DBL_MAX == doubleTest) && ERANGE == errno) {
		fprintf(stderr, "\n%s out of range of type double.\n", buff);
	}
	else {
		if ((doubleTest >= minVal) && (doubleTest <= maxVal)) {
			printf("\n%0.2f is a valid value\n", doubleTest);
			*validDouble = doubleTest;
			valid = true;
		}
		else {
			printf("\n%0.2f is not within a valid range\n", doubleTest);
			printf("Please enter a valid value between %d and %d.\n", minVal, maxVal);
		}
	}
	return valid;
}

bool getValidInt(char* buff, int* const validInt) { //function for validating credit card
	bool valid = false;
	char* endPtr;
	errno = 0;
	int intTest = 0;

	intTest = strtod(buff, &endPtr); // convert string to double and put in doubleTest, if theres anything other than numbers then put in endPtr

	if (endPtr == buff) {
		fprintf(stderr, "\n%s is not a decimal number\n", buff);
	}
	else if ('\0' != *endPtr) {
		fprintf(stderr, "\n%s: extra characters at end of input: %s\n", buff, endPtr);
	}
	else if ((INT_MIN == intTest || INT_MAX == intTest) && ERANGE == errno) {
		fprintf(stderr, "\n%s out of range of type int \n", buff);
	}
	else {
		valid = true;
	}
	return valid;
}

bool getValidChar(char* buff, char* const validChar) {// to validate size and color 
	errno = 0;
	bool valid = false;

	size_t length = strlen(buff);

	if (length == 1) {
		char* charTest = strpbrk(validChar, buff);
		if (charTest != NULL) {
			valid = true;
		}
		else {
			valid = false;
		}
	}
	else {
		valid = false;
	}
	return valid;
}
