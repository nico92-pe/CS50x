#include <cs50.h>
#include <stdio.h>

void pyramid(int n);

int main(void)
{
    // Prompt number from user

    int number;
    do
    {
        number = get_int("Number of blocks: ");
    }
    while (number < 1 || number > 8);

    // Make pyramid

    pyramid(number);

}

void pyramid(int n)
{
    for (int j = 0; j < n; j++)
    {

        // Making the spaces
        for (int i = 0; i < n - j - 1; i++)
        {
            printf(" ");
        }

        // Making the #
        for (int k = 0; k < j + 1; k++)
        {
            printf("#");
        }

        printf("\n");

    }
}
