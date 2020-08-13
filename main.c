#include <stdio.h>
#include "c/dirent.h"
#include <sys/stat.h>

int main()
{
    DIR *folder;
    struct dirent *entry;
    struct stat filestat;

    folder = opendir("./");
    if(folder == NULL)
    {
        perror("Unable to read directory");
        return(1);
    }

    /* Read directory entries */
    while( (entry=readdir(folder)) )
    {
        stat(entry->d_name,&filestat);
        if( S_ISDIR(filestat.st_mode) )
            printf("%4s: %s\n","Dir",entry->d_name);
        else
            printf("%4s: %s\n","File",entry->d_name);
    }
    closedir(folder);

    return(0);
}