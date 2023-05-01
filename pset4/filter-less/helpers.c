#include "helpers.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Create average variable
    int average = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculate average and asign it to each pixel
            average = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Create the sepia temp variables
    int sepiaRed = 0;
    int sepiaGreen = 0;
    int sepiaBlue = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculate the sepia variables
            sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
            // Check if sepia is over 255 and change it to 255
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            // Asign sepia to each pixel
            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtRed = sepiaRed;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Creat temporary variables from right
    int rightBlue = 0;
    int rightGreen = 0;
    int rightRed = 0;

    // Create temporary variables from left
    int leftBlue = 0;
    int leftGreen = 0;
    int leftRed = 0;

    // Create variable for the number of iterations
    int width_iterations = width / 2;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width_iterations; j++)
        {
            // Asign the right values to the temporary variables
            rightBlue = image[i][width - 1 - j].rgbtBlue;
            rightGreen = image[i][width - 1 - j].rgbtGreen;
            rightRed = image[i][width - 1 - j].rgbtRed;

            // Asign the left values to the temporary variables
            leftBlue = image[i][j].rgbtBlue;
            leftGreen = image[i][j].rgbtGreen;
            leftRed = image[i][j].rgbtRed;

            // Asign the lef temporary variables to the right part of the image
            image[i][width - 1 - j].rgbtBlue = leftBlue;
            image[i][width - 1 - j].rgbtGreen = leftGreen;
            image[i][width - 1 - j].rgbtRed = leftRed;

            // Asign the right temporary variables to the left part of the image
            image[i][j].rgbtBlue = rightBlue;
            image[i][j].rgbtGreen = rightGreen;
            image[i][j].rgbtRed = rightRed;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{

    // Create temporary variable to story the blur
    RGBTRIPLE(*temp_image)[width] = calloc(height, width * sizeof(RGBTRIPLE));
    // Create temporary variables to calculate the average to blur
    int averageRed = 0;
    int averageGreen = 0;
    int averageBlue = 0;

    float counter = 0.00;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Reset variables
            averageRed = 0;
            averageGreen = 0;
            averageBlue = 0;
            counter = 0.00;

            // Iterate 9 times over the evaluated pixel
            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    // Check if the pixel is in the same image
                    if ((i + k >= 0) && (i + k < height) && ((j + l) < width) && ((j + l) >= 0))
                    {
                        // If exists, summ it
                        averageRed = averageRed + image[i + k][j + l].rgbtRed;
                        averageGreen = averageGreen + image[i + k][j + l].rgbtGreen;
                        averageBlue = averageBlue + image[i + k][j + l].rgbtBlue;
                        counter++;
                    }
                }
            }

            // Calculate the average of each color
            averageRed = round(averageRed / counter);
            averageGreen = round(averageGreen / counter);
            averageBlue = round(averageBlue / counter);

            // Asign it to the temporary variable
            temp_image[i][j].rgbtBlue = averageBlue;
            temp_image[i][j].rgbtGreen = averageGreen;
            temp_image[i][j].rgbtRed = averageRed;
        }
    }

    // Asign the temporary variable to the created file
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtBlue = temp_image[i][j].rgbtBlue;
            image[i][j].rgbtGreen = temp_image[i][j].rgbtGreen;
            image[i][j].rgbtRed = temp_image[i][j].rgbtRed;
        }
    }
    
    // Free the temporary variable
    free(temp_image);

    return;
}
