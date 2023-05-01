// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // TODO: Read samples from input file and write updated data to output file

    // Open, read and write header
    uint8_t *header = malloc(HEADER_SIZE);
    fread(header, HEADER_SIZE, 1, input);
    fwrite(header, HEADER_SIZE, 1, output);

    // Open, read and write file with updated data
    float factor = atof(argv[3]);
    int16_t *buffer = malloc(sizeof(int16_t));
    while (fread(buffer, sizeof(int16_t), 1, input))
    {
        // Update volume
        *buffer *= factor;
        fwrite(buffer, sizeof(int16_t), 1, output);
    }

    free(header);
    free(buffer);

    // Close files
    fclose(input);
    fclose(output);

}
