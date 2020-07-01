#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void handle_input();
void handle_command(char command[]);

/* Basic user input function. */
void handle_input() {

    char input[100];
    // prompt text
    printf("--> ");
    // getting input
    fgets(input, 15, stdin);
    
    int result = strcmp(input, "exit");

    if (result == 10) {
        printf("handling exit coomand");
        exit(0);
    } else {
        handle_command(result);
        handle_input();

    }

}

void handle_command(char command[]) {
    printf("\nhandling command %s", command);
}



int main() 
{
    printf("q-shell v1\n");
    handle_input();



    return 0;
}