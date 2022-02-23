# Declare the assembly flavor to use the intel syntax.
.intel_syntax noprefix

# Define a symbol to be exported from this file.
.global my_function

# Declare symbol type to be a function.
.type my_function, @function

# Code follows below.

# We will follow this code:
# if(n<=0): return 0;
# if(n==1): return 1;
# else:
#   return fib(n-1)^2 + fib(n-2)^2

my_function:
    PUSH EBP
    MOV  EBP, ESP
    SUB  ESP, 4
    MOV  EAX, [EBP+8]
    #JMP _FINISH
    
    #If section
    CMP EAX, 1
    JE _IF1
    CMP EAX, 0
    JLE _IF0
    
    #Else section
    DEC EAX             # Fib(n-1)
    PUSH EAX            
    CALL my_function
    IMUL EAX, EAX       # Fib(n-1)^2
    MOV [EBP-4], EAX    # Stroting the value
    
    DEC DWORD PTR [ESP] # Fib(n-2)
    CALL my_function    
    ADD ESP, 4
    IMUL EAX, EAX       # Fib(n-2)^2
    ADD EAX, [EBP-4]    # +Fib(n-1)^2
    JMP _FINISH

_IF0:
    MOV EAX, 0          # Return 0
    JMP _FINISH

_IF1:                   # Return 1
    MOV EAX, 1

_FINISH:
    MOV ESP, EBP
    POP EBP
    RET
    
