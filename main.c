#include <stdio.h>
#include <stdlib.h>

#include "c/bmath.h"

int main() {

    printf("%d\n", (int) bm_map(2, 0, 10, 0, 100));
    printf("%f\n\n", bm_map(34, 0, 100, 5 , 7));

    printf("%f\n", bm_clamp(0, -3, 4));
    printf("%f\n", bm_clamp(-4, -3, 4));
    printf("%f\n", bm_clamp(12, -3, 4));
    
    return 0;
}

