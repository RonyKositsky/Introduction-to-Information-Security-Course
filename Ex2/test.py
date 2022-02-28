class RepeatedKeyCipher:

    def __init__(self, key: bytes = bytes([0, 0, 0, 0, 0])):
        """Initializes the object with a list of integers between 0 and 255."""
        # WARNING: DON'T EDIT THIS FUNCTION!
        self.key = list(key)

    def encrypt(self, plaintext: str) -> bytes:
        """Encrypts a given plaintext string and returns the ciphertext."""
        str_as_bytes = bytearray(plaintext.encode())
        key_as_bytes = bytearray(self.key)
        key_len = len(key_as_bytes)

        # If we have no key, we won't XOR anything.
        if key_len == 0:
            return plaintext.encode()

        counter = 0
        arr = []
        for b in str_as_bytes:
            arr.append(b ^ key_as_bytes[counter])
            
            # If the text is longer we will count the key length and then set it to zero when we will reach the end of it.
            counter += 1
            if counter == key_len:
                counter = 0

        return bytes(arr)

    def decrypt(self, ciphertext: bytes) -> str:
        """Decrypts a given ciphertext string and returns the plaintext."""
        return (self.encrypt(ciphertext.decode())).decode()

print("************")
print("Encrypt")
Cipher = RepeatedKeyCipher()
a = Cipher.encrypt("abcab")
print(bytearray(a).decode())
print(Cipher.encrypt("abcab").decode())
print("************")
print("De")
print((Cipher.encrypt(bytearray(a).decode()).decode()))

