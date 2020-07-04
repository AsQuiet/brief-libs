#if !defined(BRIEFCPP_LIB)

namespace bstring {
    bool is_eql         (char *str, char *str2);
    void copy_string    (char *dst, const char *src);
    void rstrip         (char *dst, char *src);
}

namespace bstring {

    bool is_eql(char *str, char *str2) {

        bool result = true;

        while (*str && *str != '\n') {
            result = result && (*str) == (*str2);
            (str++);
            (str2++);
        }
        return result;
    }

    void copy_string(char *dst, const char *src) {
        
        while (*src) {
            *dst = *src;
            (dst++);
            (src++);
        }

    }

    void rstrip(char *dst, char *src) {
        char nope = '\n';
        while (*src) {
            if (*src != nope) {
                *dst = *src;
            }
            (dst++);
            (src++);
        }
    }

}


namespace bio {

    void input(char *input_dst, int length);
    void input(char *input_dst);
    void clrscr();
    
    namespace os {
        int get_line_count(char *file_name);
        char **get_lines_of_file(char *file_name, int amt_lines, int width_lines);
        void print_lines(char **lines, int amt_lines);
    }
}   


namespace bio {

    typedef struct
    {
        char path[50];
    } path;

    /* Prompts the user for input and stores said input into the given string. */
    void input(char *input_dst, int length) {
        std::fgets(input_dst, length, stdin);
    }       

    /* Prompts the user for input and stores said input into the given string. 50 will the max length for the input. */
    void input(char *input_dst) {
        bio::input(input_dst, 50);
    }

    /** Clears out the command line. ¨*/
    void clrscr() {
        system("@cls||clear");
    }

    /* Contains functions for handling file data etc..*/
    namespace os {

        /** Returns the amount of lines in the file at the given path. */
        int get_line_count(char *file_name) {

            std::FILE *ptr = std::fopen(file_name, "r");

            char current_file_char = std::getc(ptr);
            int amt_lines = 0;

            while (current_file_char != EOF) {
                if (current_file_char == '\n') {
                    amt_lines++;
                }
                current_file_char = std::getc(ptr);
            }

            std::fclose(ptr);
            return amt_lines;

        }

        /** Returns all of the lines in a file. */
        char **get_lines_of_file(char *file_name, int amt_lines, int width_lines) {

            std::FILE *ptr = std::fopen(file_name, "r");

            char **lines = (char**) std::malloc(amt_lines * sizeof(char*));

            for (int i = 0; i < amt_lines; i++) {
                lines[i] = (char*) std::malloc(width_lines * sizeof(char*));
                std::fgets(lines[i],width_lines, ptr);
            }

            std::fclose(ptr);
            return lines;
        }

        /** Prints out all of the given lines. */
        void print_lines(char **lines, int amt_lines) {
            for (int i = 0; i < amt_lines; i++) {
                std::cout << lines[i];
            }
        }

    }
    
}

namespace dyn {
    typedef struct
    {
        char **list;
        int length;
    } list_strings;

    typedef struct
    {
        int *list;
    } list_ints;

    list_strings create_strings(int length);
    void set_length(list_strings list, int length);

}

namespace dyn {

    list_strings create_strings(int length) {
        list_strings list;
        list.list = (char**) std::malloc(length * sizeof(char*));
        list.length = length;
        return list;
    }

    void set_length(list_strings list, int length) {
        list.list = (char**) std::realloc(list.list, length * sizeof(char*));   
        list.length = length;
    }

}


#define BRIEFCPP_LIB
#endif