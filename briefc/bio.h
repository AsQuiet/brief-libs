#if !defined(BIO_LIB)

int     bio_get_file_lines              (char *name);
char    **bio_alloc_lines_of_file       (char *path, int amt_lines, int line_width);
void    bio_print_lines_of_file         (char **lines, int amt_lines);

#define LEN(x)  (sizeof(x) / sizeof((x)[0]))

#define BIO_LIB
#endif

#if !defined(fopen)
#include <stdio.h>
#endif

#if !defined(malloc)
#include <stdlib.h>
#endif

/** Returns the amount of lines inside the given file at the given path. */
int bio_get_file_lines(char *name) {

    FILE *fileptr = fopen(name, "r");
    int amt_lines = 0;
    char chr;

    // extract character from file and store in chr
    chr = getc(fileptr);

    if (chr != EOF) {amt_lines = 1;}
    while (chr != EOF) {
        if (chr == '\n') {
            amt_lines = amt_lines + 1;
        }
        chr = getc(fileptr);
    }
    fclose(fileptr);

    return amt_lines;
}

/** Returns a pointer to a 2D array of characters, each string being a line of the file at the given path. */
char **bio_alloc_lines_of_file(char *path, int amt_lines, int line_width) {

    // int amt_lines = bio_get_file_lines(path);
    // simply create a empty file or a 2D array of char being 1x1
    if (amt_lines == 0) {
        char **empty_file = malloc(sizeof(char*));
        empty_file[0] = malloc(sizeof(char*));
        return empty_file;
    }

    FILE *fileptr = fopen(path, "r");
    char **file_lines = malloc(sizeof(char*) * amt_lines);

    for (int i = 0; i < amt_lines; i++) {
        file_lines[i] = malloc(sizeof(char*) * line_width);
        // reading the file
        fgets(file_lines[i], line_width, fileptr);
    }

    fclose(fileptr);
    return file_lines;

}

/** Prints out the given lines. */
void bio_print_lines_of_file(char **lines, int amt_lines) {
    for(int x = 0; x < amt_lines; x++) {
        printf("%s", lines[x]);
    } 
}
