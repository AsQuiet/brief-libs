#include <stdio.h>
#include <stdlib.h>

#include "c/bcereal.h"




int main() {

    int *towrite = malloc(3);

    towrite[0] = 12;
    towrite[1] = 14;
    towrite[2] = 2;
    
    FILE *fptr = fopen("savedata.save", "rb");
    unsigned char buffer[100];

    // fwrite(towrite, sizeof(int), 3, fptr);
    fread(buffer,sizeof(buffer),3,fptr); 

    fclose(fptr);

    for (int i = 0; i< 24; i++)
        printf("%x", buffer[i]);
    printf("\n");

    return 0;
}

