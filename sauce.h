#if !defined printf
#include <stdio.h>
#endif 

#if !defined malloc
#include <stdlib.h>
#endif

#if !defined(SOUCE_H)
#define SOUCE_H

void scstart(const char*path);

void scwrite_int(const char *path, int *n);
void scwrite_int_ptr(const char *path, int *n, int ptr_length);

void scwrite_char(const char *path, char *c);
void scwrite_char_ptr(const char *path, char *str, int ptr_length);

void scwrite_double(const char *path, double *n);
void scwrite_double_ptr(const char *path, double *ptr, int ptr_length);

void scread_int(const char *path, int *n);
void scread_int_ptr(const char *path, int *n, int ptr_length);


#endif

void scstart(const char *path)
{
    fclose(fopen(path, "wb"));
}

void scwrite_int(const char *path, int *n)
{
    FILE *file = fopen(path, "ab");
    fwrite(n, sizeof(int), 1, file);
    fclose(file);
}

void scwrite_int_ptr(const char *path, int *n, int ptr_length)
{
    FILE *file = fopen(path, "ab");
    fwrite(n, sizeof(int), ptr_length, file);
    fclose(file);
}

void scread_int(const char *path, int *n)
{
    FILE *file = fopen(path, "rb");
    fread(n, sizeof(int), 1, file);
    fclose(file);
}

void scread_int_ptr(const char *path, int *n, int ptr_length)
{
    FILE *file = fopen(path, "rb");
    fread(n, sizeof(int), ptr_length, file);
    fclose(file);
}


void scwrite_char(const char *path, char *c)
{
    FILE *file = fopen(path, "ab");
    fwrite(c, sizeof(char), 1, file);
    fclose(file);
}

void scwrite_char_ptr(const char *path, char *str, int ptr_length)
{
    FILE *file = fopen(path, "ab");
    fwrite(str, sizeof(char), ptr_length, file);
    fclose(file);
}

void scread_char(const char *path, char *c)
{
    FILE *file = fopen(path, "rb");
    fread(c, sizeof(char), 1, file);
    fclose(file);
}

void scread_char_ptr(const char *path, char *str, int ptr_length)
{
    FILE *file = fopen(path, "rb");

    int *ptr = malloc(sizeof(int) * 4);

    fread(ptr, sizeof(int), 4, file);
    fread(str, sizeof(char), ptr_length, file);
    
    fclose(file);
}