#include <cs50.h>
#include <stdio.h>

long get_card_number(void);
long sum_numbers(long card);
void type(long card);

int main(void)
{
    //Ask the card number
    long card = get_card_number();
    //Get the sum of the numbers by the rules given in the instructions
    int sumar = sum_numbers(card);
    //The condition to return the card type or the Invalid
    if (sumar % 10 == 0)
    {
        type(card);
    }
    else
    {
        printf("INVALID\n");
    }

}

long get_card_number(void)
{
    // Prompt the user for card number
    long card;
    do
    {
        card = get_long("Tell me your card number: ");
    }
    while (card < 0);

    //Return the card number given by the user
    return card;
}

long sum_numbers(long card)
{
    //Initialize the variables
    int remainder, even = 0, counter = 1;

    //Loop to sum the digits
    do
    {
        remainder = card % 10;

        //Sum the even if the condition is true
        if (counter % 2 > 0)
        {
            even = even + remainder;
        }
        else //Sum the odd if the condition is false
        {
            if (remainder * 2 > 9)
            {
                even = even + 1 + (remainder * 2) % 10; // Esta pendiente partir en 2 si es que es un numero de 2 digitos
            }
            else
            {
                even = even + remainder * 2; // Esta pendiente partir en 2 si es que es un numero de 2 digitos
            }
        }

        counter++;
        card = (card - remainder) / 10;
    }
    while (card > 0);

    return even;
}

void type(long card)
{
    //Decide if the card's brand or if it is Invalid
    int reminder, even = 0, counter = 1, number13 = 0, number14 = 0, number15 = 0, number16 = 0;

    do
    {
        reminder = card % 10;

        //Getting the numbers in each placeholder
        if (counter == 13)
        {
            number13 = reminder;
        }
        else if (counter == 14)
        {
            number14 = reminder;
        }
        else if (counter == 15)
        {
            number15 = reminder;
        }
        else if (counter == 16)
        {
            number16 = reminder;
        }

        counter++;
        card = (card - reminder) / 10;
    }
    while (card > 0);

    counter--;

    //Naming the card name by its type
    if ((counter == 15) & (number15 == 3) & ((number14 == 4) || (number14 == 7)))
    {
        printf("AMEX\n");
    }
    else if ((counter == 16) & (number16 == 5) & ((number15 == 1) || (number15 == 2) || (number15 == 3) || (number15 == 4)
             || (number15 == 5)))
    {
        printf("MASTERCARD\n");
    }
    else if (((counter == 13) & (number13 == 4)) || ((counter == 16) & (number16 == 4)))
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }

}