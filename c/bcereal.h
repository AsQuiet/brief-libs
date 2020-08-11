#if !defined printf
#include <stdio.h>
#endif 

#if !defined malloc
#include <stdlib.h>
#endif

#if !defined(BCEREAL_H)
#define BCEREAL_H

typedef struct
{
    int *bits;
    int bit_amount;
} b_byte;


b_byte byte_from_size(int size_);

b_byte convert_int(int n);
b_byte convert_char(char n);


void print_b_byte(b_byte *b);

#endif

b_byte byte_from_size(int size_)
{
    b_byte b;
    b.bit_amount = size_;
    b.bits = (int*) malloc(b.bit_amount);
    return b;
}

b_byte convert_int(int n)
{
    b_byte b = byte_from_size(sizeof(n) * 8);

    for (int i = b.bit_amount-1; i >= 0; i--)
    {
        int bit = (n & (1u << i)) ? 1 : 0;
        b.bits[b.bit_amount-i-1] = bit;
    }
    
    return b;
}

b_byte convert_char(char n)
{
    b_byte b = byte_from_size(sizeof(n) * 8);

    for (int i = b.bit_amount-1; i >= 0; i--)
    {
        int bit = (n & (1u << i)) ? 1 : 0;
        b.bits[b.bit_amount-i-1] = bit;
    }
    
    return b;
}



void print_b_byte(b_byte *b)
{
    for (int i = 0; i < b->bit_amount; i++)
    {
        printf("%d", b->bits[i]);

        if ((i+1) % 8 == 0 && i != 0)
            printf(" ");            
    }
    printf("\n");
}