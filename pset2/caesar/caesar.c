#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int only_digits(string number);

int main(int argc, string argv[])
{

    // Check if it has just two arguments
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    bool is_number = only_digits(argv[1]);

    // Check if it is number
    if (is_number == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Creating the variables of texts
    string plain_text = get_string("plaintext: ");
    int long_plain_text = strlen(plain_text);
    char cipher_text[long_plain_text - 1];

    // Changing the values
    int k = atoi(argv[1]);
    int a = (int) plain_text[0];
    int cipher = 0;
    int num = 0;

    // Include ciphertext
    printf("ciphertext: ");
    for (int i = 0; i < long_plain_text; i++)
    {
        // For Mayus
        if (plain_text[i] >= 65 && plain_text[i] <= 90)
        {
            cipher = ((int) plain_text[i] - 65 + k) % 26;
            num = cipher + 65;
            cipher_text[i] = (char) num;
        }
        // For Minus
        else if (plain_text[i] >= 97 && plain_text[i] <= 122)
        {
            cipher = ((int) plain_text[i] - 97 + k) % 26;
            num = cipher + 97;
            cipher_text[i] = (char) num;
        }
        // Non text
        else
        {
            cipher_text[i] = plain_text[i];
        }

        printf("%c", cipher_text[i]);
    }
    printf("\n");
    return 0;
}

int only_digits(string number)
{

    // Calculating if the chars are numbers
    int lenght = strlen(number);
    int evaluation = 0; // To distinct if it is not a number
    for (int i = 0; i < lenght; i++)
    {
        if (isdigit(number[i]))
        {
        }
        else
        {
            evaluation++;
        }
    }

    // Check if it was a number or not
    if (evaluation > 0)
    {
        return false;
    }
    else
    {
        return true;
    }
}