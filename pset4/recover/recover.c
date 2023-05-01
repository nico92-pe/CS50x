#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    // Image size
    const int BLOCK_SIZE = 512;

    // Rename the Byte variable
    typedef uint8_t  BYTE;

    // Remember filenames
    char *infile_name = argv[1];

    // Check if there are two arguments.
    if (argc != 2)
    {
        printf("Usage: ./recover filename.raw\n");
        return 1;
    }

    // Open the raw file.
    FILE *rawfile = fopen(argv[1], "r"); //A VER SI ESTE ERA PROBLEMA
    if (rawfile == NULL)
    {
        printf("Could not open %s.\n", infile_name);
        return 1;
    }

    // FILE *output = fopen(infile_name, "r");
    BYTE *buffer = malloc(BLOCK_SIZE);

    // Creating images counter
    int count = 0;

    // Create the file name
    char *jpg_name = malloc(8 * sizeof(char));

    // Create and open the file
    FILE *img = NULL;

    // Read the file in blocks of JPGEs
    while (fread(buffer, 1, BLOCK_SIZE, rawfile) == BLOCK_SIZE)
    {

        // Check if it is an image or not
        if ((buffer[0] == 0xff) && (buffer[1] == 0xd8) && (buffer[2] == 0xff) && ((buffer[3] & 0xf0) == 0xe0))
        {
            // Free memory if it will start a new file
            if (count > 0)
            {
                fclose(img);
            }
            
            // Create the file name
            sprintf(jpg_name, "%03i.jpg", count);

            // Open the file with the new file name
            img = fopen(jpg_name, "w");

            // Counter +1 for next image found
            count++;
        }
        if (img != NULL)
        {
            fwrite(buffer, 1, BLOCK_SIZE, img);
        }
    }
    free(jpg_name);
    fclose(rawfile);
    fclose(img);
    free(buffer);
}