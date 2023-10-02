#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long number = get_long("Number?");
    long a = number;
    int count=0;
    int sum_mult = 0;
    int total = 0;

    while (a!=0){
        a=a/10;
        count++;
    }


    int digits[count];
    int dd[2];
    int doublee;

    for(int i = 0; i < count; i++){
        digits[i] = number % 10;
        number = number / 10;
    }

    for(int i=1; i<count;i = i+2){
        doublee = digits[i]*2;
        if(doublee >= 10){
            for(int j = 0; j < 2; j++){
                dd[j] = (doublee) % 10;
                doublee = (doublee) / 10;
            }

            sum_mult = sum_mult + dd[0] + dd[1];
        }
        else{
            sum_mult = sum_mult + (doublee);
        }
    }

    for(int i=0;i<count;i=i+2){
        total = total + digits[i];
    }

    total = total + sum_mult;



    if ( total % 10 == 0){
        if( digits[count-1]== 4){
            printf("VISA\n");
        }
        else if(digits[count-1] == 5 ){
            if( digits[count-2] == 1 || digits[count-2] == 2 || digits[count-2] == 3 || digits[count-2] == 4 || digits[count-2] == 5 ){
                printf("MASTERCARD\n");
            }
            else{
                printf("INVALID\n");
            }
        }
        else if(digits[count-1] == 3){
            if(digits[count-2] == 4 || digits[count-2] == 7){
                printf("AMEX\n");
            }
            else{
                printf("INVALID\n");
            }
        }
        else{
            printf("INVALID\n");
        }
    }
    else{
        printf("INVALID\n");
    }



}
