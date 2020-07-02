#include <stdio.h>
#include <stdlib.h>

#include "briefc/bio.h"

int main() {

    int amt = bio_get_file_lines("d.txt");
    char **lines = bio_alloc_lines_of_file("d.txt", amt, 20);
    bio_print_lines_of_file(lines, amt);


    return 0;
}

