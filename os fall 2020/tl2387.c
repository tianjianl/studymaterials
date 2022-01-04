#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main()
{
    char command[100];
    while(1) {
        printf("lab1>");
        scanf("%s", command);
        printf("Parent Process %d\n",getpid());
        
        if(strcmp(command,"printid") == 0) {
            printf("The ID of the current process is %d\n", getpid());
        }
        else if(strcmp(command, "exit") == 0) {
            exit(0);
        }
        else if(strcmp(command, "greet") == 0) {
            printf("Hello\n");
        }
        else {
            pid_t pid = fork();
            if(pid == 0) {
                printf("Child process %d will execute the command %s\n", getpid(), command);
                char s[20] = "/bin/";
                strcat(s,command);
                char *progname[] = {command, NULL};
                execve(s,progname,NULL);
                
                printf("Command %s not found!\n",command);
            }
        }
        int status;
        wait(&status);
    }
    return 0;
}
