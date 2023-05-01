#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_words(string words);
int count_letters(string words);
int count_sentences(string words);

int main(void)
{
    string text = get_string("Text: ");


    // Count the letters and words
    int number_words = count_words(text);
    int number_letters = count_letters(text);
    int number_sentences = count_sentences(text);

    // Calculating parameters
    float L = (float) number_letters / number_words * 100;
    float S = (float) number_sentences / number_words * 100;

    printf("letras: %i, palabras: %i, oraciones: %i\n", number_letters, number_words, number_sentences);
    printf("L: %f, S: %f\n", L, S);
    // Calculating the index
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    // Printing the grade

    if (index < 2)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

// Counting words
int count_words(string words)
{
    int text_lenght = strlen(words);
    int number_words = 0;
    int letter = 0;

    // For loop to count
    for (int i = 0; i < text_lenght; i++)
    {
        if ((int) words[i] == 32)
        {
            number_words = number_words + 1;
        }
    }
    number_words = number_words + 1;
    return number_words;
}

// Counting letters
int count_letters(string words)
{
    int text_lenght = strlen(words);
    int number_letters = 0;
    int letter = 0;

    // For loop to count
    for (int i = 0; i < text_lenght; i++)
    {
        if ((int) toupper(words[i]) >= 65 && (int) toupper(words[i]) <= 90)
        {
            number_letters = number_letters + 1;
        }
    }
    return number_letters;
}

// Counting sentences
int count_sentences(string words)
{
    int text_lenght = strlen(words);
    int number_sentences = 0;
    int letter = 0;

    // For loop to count
    for (int i = 0; i < text_lenght; i++)
    {
        if ((int) toupper(words[i]) == 33 || (int) toupper(words[i]) == 46 || (int) toupper(words[i]) == 63)
        {
            number_sentences = number_sentences + 1;
        }
    }
    return number_sentences;
}