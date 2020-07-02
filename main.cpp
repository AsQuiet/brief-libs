#include <iostream>
#include "briefcpp/brief.hpp"


void get_input() {

    // uuhuhm
    std::cout << "\nnameless~ ";

    // asking for input
    char command[50];
    bio::input(command, 50);

    // looking out for exit command
    if (bstring::is_eql("exit", command)) {
        exit(0);
    }  
    if (bstring::is_eql("clear", command)) {
        bio::clrscr();
    } else {
        std::cout<<"\n"<<command;
    }
    get_input();
}

int main() {

    get_input();

    return 0;

}
