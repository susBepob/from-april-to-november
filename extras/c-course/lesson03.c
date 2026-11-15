#include <stdio.h>

int main(void) {
    printf("-- precedence --\n");
    printf("2 + 3 * 4   = %d\n", 2 + 3 * 4);
    printf("(2+3) * 4   = %d\n", (2 + 3) * 4);
    printf("20 / 4 / 2  = %d\n", 20 / 4 / 2);
    printf("20 / (4/2)  = %d\n", 20 / (4 / 2));

    printf("\n-- negative div and mod --\n");
    printf("-7 / 3 = %d   -7 %% 3 = %d\n", -7 / 3, -7 % 3);
    printf(" 7 /-3 = %d    7 %%-3 = %d\n", 7 / -3, 7 % -3);

    printf("\n-- post vs pre --\n");
    int y = 5;
    printf("y++ gives %d, y is now %d\n", y++, y);
    y = 5;
    printf("++y gives %d, y is now %d\n", ++y, y);

    printf("\n-- compound --\n");
    int x = 10;
    printf("x += 5 -> %d\n", x += 5);
    printf("x *= 2 -> %d\n", x *= 2);
    printf("x /= 3 -> %d\n", x /= 3);

    printf("\n-- chained --\n");
    int a, b, c;
    a = b = c = 99;
    printf("a=%d b=%d c=%d\n", a, b, c);

    printf("\n-- the classic exam question --\n");
    int p = 10, q = 3;
    p -= q++;
    printf("after p -= q++ : p=%d q=%d\n", p, q);

    printf("\n-- assignment is an expression --\n");
    int z;
    printf("printf of (z = 42) prints %d, z is %d\n", z = 42, z);

    return 0;
}
