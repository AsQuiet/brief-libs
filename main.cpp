#include <iostream>
#include <string.h>
#include <vector>

#include "briefcpp/brief.hpp"
#include "main.hpp"

namespace Icarus {

    namespace cmds {
        std::string exit_ = "exit";
        std::string clear_ = "clear";
    }

    void get_input() {
        std::cout << "nameless~ ";

        IcarusCommand command;
        std::fgets(command.command, 256, stdin);

        Icarus::handle_command(command);    
    }

    void handle_command(IcarusCommand command) {

        // converting to an std::string an removing '\n'
        std::string command_string;
        command_string.assign(command.command);
        command_string.erase(command_string.end()-1);
        // std::cout << "got_input : " << command_string<<"\n";

        if (command_string.compare(Icarus::cmds::exit_) == 0) {
            exit(0);
        }

        if (command_string.compare(Icarus::cmds::clear_) == 0) {
            bio::clrscr();
        }
        
        Icarus::get_input();
    }

}

int main() {

    Icarus::get_input();

    return 0;
}

