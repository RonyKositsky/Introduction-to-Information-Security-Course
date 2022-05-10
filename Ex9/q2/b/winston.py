import socket
from Crypto.Cipher import AES
from Crypto import Random
from cryptography.hazmat.primitives import padding 

KEY = b'v9y$B&E)H@McQfTj'

def send_message(ip: str, port: int):
    """Send an *encrypted* message to the given ip + port.

    Julia expects the message to be encrypted, so re-implement this function accordingly.

    Notes:
    1. The encryption is based on AES.
    2. Julia and Winston already have a common shared key, just define it on your own.
    3. Mind the padding! AES works in blocks of 16 bytes.
    """
    
    connection = socket.socket()
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(b'I love you')
    padded_data += padder.finalize()
    
    iv = Random.new().read(AES.block_size) #choose a random, 16 byte IV
    payload = AES.new(KEY, AES.MODE_CBC, iv).encrypt(padded_data)
    
    try:
        connection.connect((ip, port))
        connection.send(iv + payload)
    finally:
        connection.close()


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    send_message('127.0.0.1', 1984)


if __name__ == '__main__':
    main()
