#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    string text = get_string("Text: ");
    int letters = 0;
    int words = 1;
    int sentences = 0;
    int length = strlen(text);

    for( int i = 0; i < length; i++){
        if(text[i] == ' '){
            words++;
        }
        else if(text[i] == '.' || text[i] == '!' || text[i] == '?'){
            sentences++;
        }
        else if(isupper(text[i]) || islower(text[i])){
            letters++;
        }
    }

    double average_n = ((double)letters/(double)words)*100;
    double average_s = ((double)sentences/(double)words)*100;

    int index = round(0.0588 * average_n - 0.296 * average_s - 15.8);

    if( index >= 16){
        printf("Grade 16+\n");
    }
    else if( index < 1){
        printf("Before Grade 1\n");

    }
    else{
        printf("Grade %d\n",index);
    }
}