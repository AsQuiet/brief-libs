#include <iostream>
#include "main.hpp"

namespace bstring
{
    char *string(const char* str);
    char *string(int length);
    char *add_char(char* str, char toAdd);
    char *concat_string(char *str, char *str2);
    bool is_eql(char *str, char *str2);
    char *remove_index(char *str, int index);
    char *remove_char(char *str, char toRemove);
    char *slice(char *str, int start, int end);
    void set_string(char *dst, char *src);
}

namespace bstring 
{
    char *string(const char* str) {

        // will indicate how much memory to alloc
        int length = std::strlen(str);
        char *str_ = (char*) std::malloc(sizeof(char*) * (length+1));
        
        while(*str) {
            *str_ = *str;
            str++;
            str_++;
        }
        // signaling the end of the string (removes thhose weird random characters fromm string)
        *str_ = 0;
        // resseting pointer
        str_ = str_ - length;

        return str_;

    }

    char *string(int length) {
        char *str = (char*) std::malloc(sizeof(char*) * length);
        return str;
    }

    char *add_char(char* str, char toAdd) {

        // will indicate how much memory to realloc
        int length = std::strlen(str);
        char *str_ = (char*) std::realloc(str, sizeof(char*) * (length+1));
        
        // adding character
        str_[length] = toAdd;
        str_[length+1] = 0;

        return str_;
    }

    char *concat_string(char* str, char* str2) {
        
        // getting the length of the two strings
        int length_str = std::strlen(str);
        int length_str2 = std::strlen(str2);

        // allocating memory
        char *str_ = (char*) std::malloc(sizeof(char*) * (length_str2 + length_str + 1));

        for (int i = 0; i < length_str; i++) {
            str_[i] = str[i];
        }
        for (int i = 0; i < length_str2; i++) {
            str_[i + length_str] = str2[i];
        }
        str_[length_str + length_str2] = 0;
        
        return str_;

    }

    bool is_eql(char *str, char *str2) {
        bool result = true;
        while (*str) {
            result = result && *str == *str2;
            str++;
            str2++;
        }
        return result;
    }

    char *remove_index(char *str, int index) {

        int length = std::strlen(str);
        char *result = (char*) std::malloc(sizeof(char*) * (length-1));

        int current_index = 0;
        while (*str) {
            if (current_index != index) {
                *result = *str;
                result++;
                str++;
            }
            current_index++;
        }
        *result = 0;
        // resseting pointer
        result = result - length + 1;

        return result;
    }

    char *remove_char(char *str, char toRemove) {

        int length = std::strlen(str);
        char *result = (char*) std::malloc(sizeof(char*) * (length));

        int length_str_ = 0;

        while (*str) {

            if (*str != toRemove) {
                *result = *str;
                result++;
                length_str_++;
            }

            str++;

        }

        *result = 0;
        result = result - length_str_;
        return result;
    }

    // start included end excluded
    char *slice(char *str, int start, int end) {
    
        int length = std::strlen(str);
        char *result = (char*) std::malloc(sizeof(char*) * (length));

        int current_index = 0;
        

        while (*str) {

            if (current_index >= start && current_index < end) {
                *result = *str;
                result++;
            }

            current_index++;
            str++;

        }
        *result = 0;
        result = result - (end - start);

        return result;
    }

    void set_string(char *dst, char *src) {
        while (*src) {
            *dst = *src;
            src++;
            dst++;
        }
    }

    char *insert_at(char *str, char toInsert, int index) {
        int length = std::strlen(str);
        char* str_ = bstring::string(length+1);
        int current_index = 0;
        while (*str) {
            if (current_index == index) {
                *str_ = toInsert;
                str_++;
            }
            *str_ = *str;
            str++;
            str_++;
            current_index++;
        }
        *str_ = 0;
        str_ = str_ - length - 1;
        return str_;
    }

}

int main() {

    char *some_string = bstring::string(5);
    bstring::set_string(some_string, "aaaaa");
    std::cout << some_string;

    return 0;
}

