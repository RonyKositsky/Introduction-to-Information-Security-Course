# Declare the assembly flavor to use the intel syntax.
.intel_syntax noprefix

# Define a symbol to be exported from this file.
.global my_function

# Declare symbol type to be a function.
.type my_function, @function

my_function:
    # This code reads the first argument from the stack into EBX.
    MOV EAX, DWORD PTR [ESP + 4]
    
    # We are saving EBX in the stack because as mentioned in the Facebook 
    # group we need to save it's original value.
    PUSH EBX
    MOV EBX, EAX

    #Checks Input. If input <= 0, Return 0. If not, start the loop.
    CMP EBX, 0
    JLE _RET_ZERO
    CMP EBX, 1      # 1 is also special scenario because 1*1 = 1
    JE _RET_ONE
    JMP _LOOP_START
    
_RET_ZERO:
    MOV EAX, 0
    JMP _RETURN
    
_RET_ONE:
    MOV EAX, 1
    JMP _RETURN

    # Main loop. We iterate over all the numbers and find if we have x s.t. x*x = EBX.
_LOOP_START:
    MOV ECX, 0 # Init counter.
    
_LOOP:
    MOV  EDX, ECX
    IMUL EDX, EDX
    CMP  EDX, EBX
    JNE   _LOOP_INC
    # Taking root value from ECX(The root is value will be in ECX, our counter).
    MOV EAX, ECX
    JMP _RETURN
     
_LOOP_INC:
    INC  ECX
    CMP  ECX, EBX
    JNE  _LOOP
    MOV EAX, 0

_RETURN:
    POP EBX
    RET


