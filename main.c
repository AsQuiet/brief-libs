#include <stdio.h>
#include <stdlib.h>

#include "briefc/bio.h"

int str_len(char *line) {
    int length = 0;

    while (*(line)) {
        length = length + 1;
        (line++);
    }

    return length;
}

int main() {

    int len = str_len("quinten");
    printf("%d", len);

    // int amt = bio_get_file_lines("d.txt");
    // char **lines = bio_alloc_lines_of_file("d.txt", amt,20);
    // bio_print_lines_of_file(lines, amt);

    return 0;
}