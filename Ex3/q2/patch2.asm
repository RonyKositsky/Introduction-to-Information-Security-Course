MOV EAX, 0x8048662;             # Jump to open file. We will skip first cycle.
JMP EAX;                          
MOVZX EAX, WORD PTR [EBP-1036]; 
CMP AL, 35;                     # Read first char, '#' sign
JNZ 109;
CMP AH, 33;                     # Read second char, '!' sign    
JNZ 109;    
LEA EAX, [EBP-1034];        
PUSH EAX;
MOV EAX, 0x8048460;             # Calling _system.
CALL EAX;
ADD ESP, 4;
MOV EAX, 0x8048662;             # Return to main function.
JMP EAX;

