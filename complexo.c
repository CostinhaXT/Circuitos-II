#include <stdio.h>
#include <complex.h>
#include <math.h>
int main() {
    double complex z1 = 1.0 + 1.0 * I;
    double complex z2 = 2.0 - 3.0 * I;
    
    printf("z1 = %.2f + %.2fi\n", creal(z1), cimag(z1));
    printf("z2 = %.2f + %.2fi\n", creal(z2), cimag(z2));


    return 0;
}