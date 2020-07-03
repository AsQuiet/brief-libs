#include <iostream>
#include "briefcpp/brief.hpp"
#include "main.hpp"

namespace Icarus {

    namespace cmds {
        char exit_[5] = "exit";
        char clear_[6] = "clear";
    }

    void get_input() {
        std::cout << "nameless~ ";
        IcarusCommand command;
        std::fgets(command.command, 256, stdin);
        Icarus::handle_command(command);
        
    }

    void handle_command(IcarusCommand command) {
        
        if (bstring::is_eql(Icarus::cmds::exit_, command.command)) {
            exit(0);
        }

        if (bstring::is_eql(Icarus::cmds::clear_, command.command)) {
            bio::clrscr();
        }

        Icarus::get_input();
    }

}

int main() {
    Icarus::get_input();
    return 0;
}

