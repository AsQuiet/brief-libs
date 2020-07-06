#include <iostream>
#include "briefcpp/brief.hpp"

int main() {

    char *some_string = bstring::string(5);
    bstring::set_string(some_string, "aaaaa");
    std::cout << some_string;

    return 0;
}

