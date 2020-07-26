#if !defined(BRIEF_LIB)

typedef struct {

    char string[50];

} bstring;



bstring         create_string       (const char *str);
void            set_string          (char *dst, const char *src);
int             is_eql              (char *str, char *str2);

#define BRIEF_LIB
#endif

void set_string(char *dst, const char *src) {

    // while the current character of src is not null (*src => returns character at current pointer location)
    while (*src) {

        // dereference the dst pointer and set that character equal to the source character
        *dst = *src;

        // incremenent the two pointers
        (dst++);
        (src++);
    }
}

// creates a string struct
bstring create_string(const char *str) {
    bstring result;
    set_string(result.string, str);
    return result;
}

int is_eql(char *str, char *str2) {
    int result = 1;
    while (*str) {
        
        result = result && ((*str) == (*str2));
        // incrementing pointer
        (str++);
        (str2++);
    }
    return result;
}