#include <stdio.h>
#include <complex.h>
#include <math.h>
int main() {
    float r1, r2, r3, r4, r5, vf, req, i;
    
    printf("INSIRA OS VALORES CONFORME SOLICITADO \n");
    printf("Tensão da Fonte (V)\n");
    scanf("%f", &vf);
    printf("Digite os valores dos resistores em ordem (R1,R2...R5 )\n");
    scanf("%f" "%f" "%f" "%f" "%f", &r1, &r2, &r3, &r4, &r5);
    
    req = ((r1+r2+r3)*(r4+r5))/((r1+r2+r3)+(r4+r5));
    i = vf/req;

    printf("REQ: %.2f Ω\nIt: %.2f A \n", req, i);

    return 0;
}