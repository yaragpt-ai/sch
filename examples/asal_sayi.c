/* === TÜRK Dili Runtime === */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int asal_mi(int sayi);

int asal_mi(int sayi) {
    if ((sayi < 2)) {
        return 0;
    }
    if ((sayi == 2)) {
        return 1;
    }
    if (((sayi % 2) == 0)) {
        return 0;
    }
    int bolen = 3;
    while (((bolen * bolen) <= sayi)) {
        if (((sayi % bolen) == 0)) {
            return 0;
        }
        bolen = (bolen + 2);
    }
    return 1;
}

int main() {
    int sayi = 1;
    while ((sayi <= 50)) {
        if (asal_mi(sayi)) {
            printf("%d\n", sayi);
        }
        sayi = (sayi + 1);
    }
    return 0;
}
