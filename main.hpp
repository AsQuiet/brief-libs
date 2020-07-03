#ifndef MAIN_H

typedef struct {
    char command[256];
} IcarusCommand;

namespace Icarus {
    namespace cmds {}
    void get_input();
    void handle_command(IcarusCommand command);
}


#define MAIN_H
#endif