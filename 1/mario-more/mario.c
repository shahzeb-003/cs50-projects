#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int spaces;
    int height;

    while( height <= 0){
        height = get_int("Height?");
    }
    
    for(int i = 1; i <= height; ++i){
        spaces = height - i;
        for(int j=0;j<spaces;++j){
            printf(" ");
        }
        for(int z=0;z<i;++z){
            printf("#");
        }
        printf("  ");
        for(int z=0;z<i;++z){
            printf("#");
        }
        printf("\n");
    }
}