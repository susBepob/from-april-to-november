#include <stdio.h>
int main(void) {
    // Make the two steps visible by stopping halfway.

    printf("STEP 1 - what the RIGHT SIDE computes, on its own:\n");
    printf("  5 / 2   as a raw expression -> %d\n", 5 / 2);
    printf("  7 / 2   as a raw expression -> %d\n", 7 / 2);
    printf("  7 / 2.0 as a raw expression -> %f\n", 7 / 2.0);

    printf("\nSTEP 2 - now put each into a box:\n");
    float  avg = 5 / 2;      // box is float... but step 1 already gave 2
    double d   = 7 / 2;      // box is double... but step 1 already gave 3
    int    x   = 7 / 2.0;    // step 1 gave 3.5, box chops it
    printf("  float  avg = 5 / 2;    -> %.1f\n", avg);
    printf("  double d   = 7 / 2;    -> %f\n", d);
    printf("  int    x   = 7 / 2.0;  -> %d\n", x);

    printf("\nTHE FIX - change step 1, not the box:\n");
    float good = (float)5 / 2;
    printf("  float good = (float)5 / 2; -> %.1f\n", good);
    return 0;
}
