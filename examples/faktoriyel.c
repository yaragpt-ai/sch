/* === TÜRK Dili Runtime === */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int faktoriyel(int n);

int faktoriyel(int n) {
    if ((n <= 1)) {
        return 1;
    }
    return (n * faktoriyel((n - 1)));
}

int main() {
    int i = 1;
    while ((i <= 5)) {
        printf("%d\n", i);
        printf("%s\n", "! =");
        printf("%d\n", faktoriyel(i));
        i = (i + 1);
    }
    return 0;
}
