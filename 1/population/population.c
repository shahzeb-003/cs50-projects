#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int start = 0;
    int end = 0;
    int years = 0;
    int born = 0;
    int pass = 0;

    while (start < 9) {
        start = get_int("What's the start? ");
    }
    while (end < start) {
        end = get_int("What's the end? ");
    }

    while (start < end ) {
        born = start/3;
        pass = start/4;
        start = start + born - pass;
        years = years + 1;

    }

    printf("Years: %d \n", years);
}
