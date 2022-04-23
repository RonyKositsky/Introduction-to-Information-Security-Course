#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int adr  = 0x65656565; // AAAA
int pid  = 0x66666666; // BBBB
int data = 0x67676767; // CCCC

int main() 
{
    int status;

    // Attaching to ptrace.
    if(ptrace(PTRACE_ATTACH, pid, NULL, NULL) == -1)
    {
        perror("Error in attach.");
        return 1;
    }
    
    // Waiting for the process to stop.
    waitpid(pid, &status, 0); 
    
    if (WIFEXITED(status)) 
    { 
        return 1;
    }
    
    // Our code.
    ptrace(PTRACE_POKEDATA, pid, adr, data);
    
    // Deatch.
    if (ptrace(PTRACE_DETACH, pid, NULL, NULL) == -1)
    {
        perror("Error in detach");
        return 1;
    } 
    
    return 0;
}
