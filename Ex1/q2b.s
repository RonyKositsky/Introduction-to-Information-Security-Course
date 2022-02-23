# Declare the assembly flavor to use the intel syntax.
.intel_syntax noprefix

# Define a symbol to be exported from this file.
.global my_function

# Declare symbol type to be a function.
.type my_function, @function

# Code follows below.

my_function:
     # This code reads the first argument from the stack into EBX.
    MOV EBX, DWORD PTR [ESP + 4]
    
    # First, we will handle the negative input, a0 and a1.
    CMP EBX, 1
    JE _IF1
    CMP EBX, 0
    JLE _IF0
    
    # If we didnt get those values we will start our iteration.
    # We will store ESI = Fib(n-1), EDX = Fib(n-2).
    # We init them to 1,0 accordingly and run the loop. In each iteration
    # we will store the value in EAX. If we didn't finish we will update
    # EDX = ESI, ESI = EAX.
    
    MOV ESI, 1
    MOV EDX, 0
    MOV ECX, 1 # Our loop counter.

_LOOP:
    MOV  EAX, EDX
    IMUL EAX, EDX # EAX = Fib(n-2)^2
    MOV  EDI, ESI
    IMUL EDI, EDI # EDI = Fib(n-1)^2
    ADD  EAX, EDI # EAX += Fib(n-1)^2
    
    # Now we will store the new values for the next iteratioc calculation.
    MOV EDX, ESI
    MOV ESI, EAX
    
    INC  ECX
    CMP  ECX, EBX
    JNE  _LOOP
    JMP _FINISH

_IF0:
    MOV EAX, 0          # Return 0
    JMP _FINISH

_IF1:                   # Return 1
    MOV EAX, 1

_FINISH:
    RET
    
