#if !defined printf
#include <stdio.h>
#endif 

#if !defined malloc
#include <stdlib.h>
#endif

#if !defined(BSERIALIZE_H)
#define BSERIALIZE_H

typedef struct
{
    FILE *fptr;
    int write;
} bserialize_t;

bserialize_t bopen_write(const char *path);
bserialize_t bopen_read(const char *path);

void bclose(bserialize_t *t);

void bserialize_int         (bserialize_t *t, int *ptr, int amount);
void bserialize_char        (bserialize_t *t, char *ptr, int length);
void bserialize_double      (bserialize_t *t, double *ptr, int amount);
void bserialize_float       (bserialize_t *t, float *ptr, int amount);

int     *bto_int_ptr(int n);
float   *bto_float_ptr(float n);
double  *bto_double_ptr(double n);
char    *bto_char_ptr(char n); 

#endif

bserialize_t bopen_write(const char *path)
{
    bserialize_t bt;
    bt.fptr = fopen(path, "wb");
    bt.write = 1;
    return bt;
}

bserialize_t bopen_read(const char *path)
{
    bserialize_t bt;
    bt.fptr = fopen(path, "rb");
    bt.write = 0;
    return bt;
}

void bclose(bserialize_t *t)
{
    fclose(t->fptr);
}

void bserialize_int(bserialize_t *t, int *ptr, int amount){
    if (t->write==1)
        fwrite(ptr, sizeof(int), amount, t->fptr);
    else
        fread(ptr, sizeof(int), amount, t->fptr);
}

void bserialize_char(bserialize_t *t, char *ptr, int length){
    if (t->write==1)
        fwrite(ptr, sizeof(char), length, t->fptr);
    else
        fread(ptr, sizeof(char), length, t->fptr);
}

void bserialize_float(bserialize_t *t, float *ptr, int amount){
    if (t->write==1)
        fwrite(ptr, sizeof(float), amount, t->fptr);
    else
        fread(ptr, sizeof(float), amount, t->fptr);
}

void bserialize_double(bserialize_t *t, double *ptr, int amount){
    if (t->write==1)
        fwrite(ptr, sizeof(double), amount, t->fptr);
    else
        fread(ptr, sizeof(double), amount, t->fptr);
}


int *bto_int_ptr(int n) {
    return &n;
}

float *bto_float_ptr(float n) {
    return &n;
}

double *bto_double_ptr(double n) {
    return &n;
}

char *bto_char_ptr(char n) {
    return &n;
}