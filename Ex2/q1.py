import itertools


class RepeatedKeyCipher:

    def __init__(self, key: bytes = bytes([0, 0, 0, 0, 0])):
        """Initializes the object with a list of integers between 0 and 255."""
        # WARNING: DON'T EDIT THIS FUNCTION!
        self.key = list(key)

    def encrypt(self, plaintext: str) -> bytes:
        """Encrypts a given plaintext string and returns the ciphertext."""
        str_as_bytes = bytearray(plaintext.encode('latin-1'))
        key_as_bytes = bytearray(self.key)
        key_len = len(key_as_bytes)

        # If we have no key, we won't XOR anything.
        if key_len == 0:
            return plaintext.encode('latin-1')

        counter = 0
        arr = []
        for b in str_as_bytes:
            arr.append(b ^ key_as_bytes[counter])

            # If the text is longer we will count the key length and then set it to zero when we will reach the end
            # of it.
            counter += 1
            if counter == key_len:
                counter = 0

        return bytes(arr)

    def decrypt(self, ciphertext: bytes) -> str:
        """Decrypts a given ciphertext string and returns the plaintext."""
        return (self.encrypt(ciphertext.decode('latin-1'))).decode('latin-1')


class BreakerAssistant:

    def plaintext_score(self, plaintext: str) -> float:
        """Scores a candidate plaintext string, higher means more likely."""
        LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz"
        score = 0
        for letter in plaintext:
            if letter in LETTERS:
                score += 1
        return score

    def brute_force(self, cipher_text: bytes, key_length: int) -> str:
        """Breaks a Repeated Key Cipher by brute-forcing all keys."""

        # Generate keys.
        key_pos = [key for key in range(256)]  # 2^8 possibilities for each byte.

        # We will generate cartesian product in the desired length.
        keys = [key for key in itertools.product(key_pos, repeat=key_length)]

        highest_score = 0
        best_key = keys[0]

        for key in keys:
            dec_text = RepeatedKeyCipher(bytes(key)).decrypt(cipher_text)
            score = self.plaintext_score(dec_text)
            if score > highest_score:
                highest_score = score
                best_key = key

        return RepeatedKeyCipher(bytes(best_key)).decrypt(cipher_text)

    def one_byte_brute_force(self, key_length, cipher_text, index):
        new_cipher = cipher_text[index::key_length]

        best_score = 0
        best_byte = 0

        for byte in range(256):
            plain_text = RepeatedKeyCipher(bytes([byte])).decrypt(new_cipher)
            cur_score = self.plaintext_score(plain_text)
            if cur_score >= best_score:
                best_byte = byte
                best_score = cur_score

        return best_byte

    def smarter_break(self, cipher_text: bytes, key_length: int) -> str:
        """Breaks a Repeated Key Cipher any way you like."""
      
        best_key = []
        for index in range(key_length):
            best_key.append(self.one_byte_brute_force(key_length, cipher_text, index))

        return RepeatedKeyCipher(bytes(best_key)).decrypt(cipher_text)

