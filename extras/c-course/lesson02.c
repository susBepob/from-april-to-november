#include <stdio.h>
#include <limits.h>
#include <float.h>

int main(void) {
    printf("=== SIZES ON THIS MACHINE (bytes) ===\n");
    printf("char        %zu\n", sizeof(char));
    printf("short       %zu\n", sizeof(short));
    printf("int         %zu\n", sizeof(int));
    printf("long        %zu\n", sizeof(long));
    printf("long long   %zu\n", sizeof(long long));
    printf("float       %zu\n", sizeof(float));
    printf("double      %zu\n", sizeof(double));
    printf("long double %zu\n", sizeof(long double));

    printf("\n=== RANGES ===\n");
    printf("int      %d .. %d\n", INT_MIN, INT_MAX);
    printf("unsigned 0 .. %u\n", UINT_MAX);
    printf("long     %ld .. %ld\n", LONG_MIN, LONG_MAX);

    printf("\n=== LITERAL NOTATIONS (all the same number) ===\n");
    printf("decimal 255 = %d\n", 255);
    printf("octal   0377 = %d\n", 0377);
    printf("hex     0xFF = %d\n", 0xFF);
    printf("careful: 010 = %d  (leading zero means OCTAL)\n", 010);

    printf("\n=== SIGNED/UNSIGNED TRAP ===\n");
    int neg = -1;
    unsigned u = 1;
    printf("is -1 < 1u ? %s\n", (neg < u) ? "yes" : "NO (!!)");
    printf("-1 seen as unsigned = %u\n", (unsigned)neg);

    printf("\n=== TRUNCATION, NOT ROUNDING ===\n");
    printf("(int)3.99  = %d\n", (int)3.99);
    printf("(int)-3.99 = %d\n", (int)-3.99);

    printf("\n=== INTEGER DIVISION vs FLOAT ===\n");
    printf("7 / 2       = %d\n", 7 / 2);
    printf("7.0 / 2     = %f\n", 7.0 / 2);
    printf("7 / 2.0     = %f\n", 7 / 2.0);

    printf("\n=== PRECISION LOSS ===\n");
    float f = 16777217.0f;
    printf("float holding 16777217 = %.1f\n", f);
    printf("float from ULLONG_MAX  = %.0f\n", (float)ULLONG_MAX);
    printf("actual  ULLONG_MAX     = %llu\n", ULLONG_MAX);

    printf("\n=== OVERFLOW WRAP (unsigned) ===\n");
    unsigned char b = 255;
    b = b + 1;
    printf("unsigned char 255 + 1 = %u\n", b);

    return 0;
}
