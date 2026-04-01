/* === TÜRK Dili Runtime === */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main() {
    int sayi = 1;
    while ((sayi <= 100)) {
        if (((sayi % 15) == 0)) {
            printf("%s\n", "FizzBuzz");
        }
        else if (((sayi % 3) == 0)) {
            printf("%s\n", "Fizz");
        }
        else if (((sayi % 5) == 0)) {
            printf("%s\n", "Buzz");
        }
        else {
            printf("%d\n", sayi);
        }
        sayi = (sayi + 1);
    }
    return 0;
}
