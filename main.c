#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "c/bcereal.h"
#include "sauce.h"

typedef struct
{
    int my_ptr_array_1;
} ptr_sizes;

typedef struct {
    int n1;
    int n2;
    int n3;
} data;

void write_()
{

    data d;
    d.n1 = 23;
    d.n2 = 13;
    d.n3 = 15;

    FILE *ptr = fopen("program.bin", "wb");

    fwrite(&d, sizeof(data), 1, ptr);
    d.n2 = 678;
    fwrite(&d, sizeof(data), 1, ptr);
    

    fclose(ptr);
}

void read_()
{
    data d;
    FILE *ptr = fopen("program.bin", "rb");

    fread(&d, sizeof(data), 1, ptr);
    printf("%d - %d - %d", d.n1, d.n2, d.n3);
    fread(&d, sizeof(data), 1, ptr);
    printf("%d - %d - %d", d.n1, d.n2, d.n3);
    fclose(ptr);

}

void write_2()
{   
    FILE *ptr = fopen("program.bin", "wb");

    int *amt = (int*) malloc(sizeof(int) * 5);
    amt[0] = 1;
    amt[1] = 4;
    amt[2] = 34;

    fwrite(&amt, sizeof(int), 3, ptr);
    fclose(ptr);
    free(amt);
    
}

void read_2()
{
    FILE *ptr = fopen("program.bin", "rb");

    int *amt = (int*) malloc(sizeof(int) * 5);

    fread(&amt, sizeof(int), 3, ptr);

    printf("0 is %d and 1 is %d and 2 is %d\n", amt[0], amt[1], amt[2]);

    fclose(ptr);
    free(amt);
}


typedef struct 
{
    char *name;
    int n1;
} bcl_savedata;

void save_file(bcl_savedata *sd, int size, const char *path)
{
    FILE *ptr = fopen(path, "wb");
    fwrite(sd, size, 1, ptr);
    fclose(ptr);
}

bcl_savedata read_file( int size, const char *path)
{
    FILE *ptr = fopen(path, "rb");
    bcl_savedata sd;
    fread(&sd, size, 1, ptr);
    fclose(ptr);
    return sd;
}



int main() 
{
    
    int *ptr = malloc(sizeof(int) * 4);
    char *name = malloc(sizeof(char) * 10);

    // ptr[0] = 23;
    // ptr[1] = 32;
    // ptr[2] = 64;
    // ptr[3] = 46;

    // scstart("program.bin");
    // scwrite_int_ptr("program.bin", ptr, 4);

    // strcpy(name, "larry");

    // scwrite_char_ptr("program.bin", name, 10);

    scread_int_ptr("program.bin", ptr, 4);
    scread_char_ptr("program.bin", name, 5);


    printf("%d - %d - %d - %d + %s\n", ptr[0], ptr[1], ptr[2], ptr[3], name);


    
    
    return 0;
}

