#include <stdio.h>
#include <stdlib.h>

// This function will be implemented in our assembly code.
int my_function();


int main(int argc, char* argv[])
{
    int input, output;

    if (argc != 2) {
        printf("USAGE: %s <number>\n", argv[0]);
        return -1;
    }

    input = atoi(argv[1]);
    output = my_function(input);

    printf("%d\n", output);

    return 0;
}
