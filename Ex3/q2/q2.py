from infosec.core import assemble


def patch_program_data(program: bytes) -> bytes:
    """
    Implement this function to return the patched program. This program should
    execute lines starting with #!, and print all other lines as-is.

    Use the `assemble` module to translate assembly to bytes. For help, in the
    command line run:

        ipython3 -c 'from infosec.core import assemble; help(assemble)'

    :param data: The bytes of the source program.
    :return: The bytes of the patched program.
    """
    program_arr = bytearray(program)    
    FIRST_OFFSET = 1587
    SECOND_OFFSET = 1485

    # First patch
    patch1_bytes = assemble.assemble_file("patch1.asm")
    patch1_bytearray = bytearray(patch1_bytes)
    for i in range(len(patch1_bytearray)):
        program_arr[FIRST_OFFSET + i] = patch1_bytearray[i]

    # Second patch
    patch2_bytes = assemble.assemble_file("patch2.asm")
    patch2_bytearray = bytearray(patch2_bytes)
    for i in range(len(patch2_bytearray)):
        program_arr[SECOND_OFFSET + i] = patch2_bytearray[i]
        
    return bytes(program_arr)


def patch_program(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    patched = patch_program_data(data)
    with open(path + '.patched', 'wb') as writer:
        writer.write(patched)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <readfile-program>'.format(argv[0]))
        return -1
    path = argv[1]
    patch_program(path)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
