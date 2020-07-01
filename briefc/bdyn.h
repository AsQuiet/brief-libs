#if !defined(BDYN_LIB)

int     *bdyn_int           (int len);
int     *bdyn_int_set       (int (*ptr), int amount);
int     bdyn_int_length     (int *ptr);

void    bdyn_print_int      (int *ptr);

#define BDYN_LIB
#endif

#if !defined(malloc)
#include <stdlib.h>
#endif

#if !defined(printf)
#include <stdio.h>
#endif

/** Creates an integer array and allocates the memory for it. The allocated memory is one more than the given length, the length of the array is saved here. To acces the length simply use *(ptr-1). */
int *bdyn_int(int len) {

    int *ptr = (int*) malloc((len + 1) * sizeof(int));
    // saving the length in the first slot of the memory
    *(ptr + 0) = len;
    return ptr + 1;

}

/** Returns the length of the given array, wich is saved in the first element of the pointer. */
int bdyn_int_length(int *ptr) {
    return *(ptr - 1);
}

/** Sets the length of the given array. */
int *bdyn_int_set(int *ptr, int amount) {

    int *ptr_new = (int*) realloc(ptr-1, (amount + 1) * sizeof(int)); 
    *(ptr_new + 0) = amount;   
    return (ptr_new + 1);

}

/** Prints out the given array. */
void bdyn_print_int(int *ptr) {
    printf("[");
    int n = bdyn_int_length(ptr);
    for (int i=0; i < n; i++) {
        printf("%d", ptr[i]);
        if (i != n - 1) printf(", ");
    }
    printf("]\n");
}
