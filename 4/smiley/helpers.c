#include "helpers.h"

void colorize(int height, int width, RGBTRIPLE image[height][width])
{

    for(int row = 0; row<width;row++){
        for(int column = 0; column < height; column++){
            if(image[column][row].rgbtBlue == 0 && image[column][row].rgbtGreen == 0 && image[column][row].rgbtRed == 0){
                image[column][row].rgbtBlue = 52;
                image[column][row].rgbtGreen = 180;
                image[column][row].rgbtRed = 235;
            }
        }
    }
}
