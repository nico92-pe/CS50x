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
        printf("Usage: ./substitution key\n");
        return 1;
    }

    bool key_correct = only_digits(argv[1]);

    if (key_correct == false)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    // Creating the variables of texts
    string plain_text = get_string("plaintext: ");
    int long_plain_text = strlen(plain_text);
    string key_text = argv[1];
    int cipher = 0;
    char cipher_text[long_plain_text - 1];

    printf("ciphertext: ");
    for (int i = 0; i < long_plain_text; i++)
    {
        if (plain_text[i] >= 65 && plain_text[i] <= 90)
        {
            cipher = ((int) plain_text[i] - 65);
            cipher_text[i] = toupper(key_text[cipher]);
        }
        // For Minus
        else if (plain_text[i] >= 97 && plain_text[i] <= 122)
        {
            cipher = ((int) plain_text[i] - 97);
            cipher_text[i] = tolower(key_text[cipher]);
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
    // Calculating if the chars are letters and are not repeated
    int lenght = strlen(number);
    int letter = 0;
    if (lenght != 26)
    {
        return false;
    }

    // Checking if repeated numbers
    char key_evaluation[lenght];
    for (int i = 0; i < lenght; i++)
    {
        letter = (int) toupper(number[i]);
        // Check if it is a letter
        if (letter >= 65 && letter <= 90)
        {
            // Evaluate if repeated numbers
            for (int j = 0; j < i; j++)
                if (letter == (int) toupper(number[j]))
                {
                    return false;
                }
        }
        else
        {
            // Exit loop, because it is not a letter
            return false;
        }
    }
    // Everything ok, return True
    return true;
}