// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Declare public variable for size
unsigned int dictionary_size = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Look for the hash of the word
    int index_checker = hash(word);

    // Create the traveler node for checking
    node *traveler = malloc(sizeof(node));
    if (traveler == NULL)
    {
        printf("Not enough space\n");
        return false;
    }

    // Check through the linked-list
    traveler = table[index_checker];
    while (traveler != NULL)
    {
        // If they are the same, return. If not, continue through the nodes.
        if (strcasecmp(traveler->word, word) == 0)
        {
            return true;
        }
        traveler = traveler->next;
    }

    // Free traveler
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary
    FILE *file_dictionary = fopen(dictionary, "r");
    if (file_dictionary == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        return false;
    }

    char word_buffer[LENGTH + 1];
    //int *dictionary_size = malloc(sizeof(int));
    //*dictionary_size = 0;

    // Read strings from file, one at a time
    while (fscanf(file_dictionary, "%s", word_buffer) != EOF)
    {
        // Create the node and check for space
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            printf("Not enough space\n");
            return false;
        }

        // Copy the word and assign the NULL character to the created node
        strcpy(n->word, word_buffer);
        n->next = NULL;

        // Hash the word of the dictionary
        unsigned int index = hash(word_buffer);

        // Assign values to the table
        n->next = table[index];
        table[index] = n;

        // Count the words
        dictionary_size++;

    }
    fclose(file_dictionary);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (dictionary_size > 0)
    {
        return dictionary_size;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        while (cursor)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
        if (cursor == NULL)
        {
            return true;
        }
    }
    return false;
}
