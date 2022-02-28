import itertools
from io import BytesIO

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
        return (self.encrypt(ciphertext.decode(encoding="ISO-8859-1"))).decode(encoding="ISO-8859-1")


class BreakerAssistant:

    def plaintext_score(self, plaintext: str) -> float:
        """Scores a candidate plaintext string, higher means more likely."""
        # Please don't return complex numbers, that would be just annoying.
        # I used this link for my idea https://crypto.stackexchange.com/questions/30209/developing-algorithm-for-detecting-plain-text-via-frequency-analysis
        # We will conduct chi suqared testing with english ASCII text.
        LETTERS_IN_ENGLISH = 26
        english_freq = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,  # A-G
                        0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,  # H-N
                        0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,  # O-U
                        0.00978, 0.02360, 0.00150, 0.01974, 0.00074]                    # V-Z
        ignored = 0
        count_arr = [0] * LETTERS_IN_ENGLISH
        for c in plaintext:
            c = ord(c)
            if c >= 65 and c <= 90:
                count_arr[c - 65] += 1;     # uppercase A-Z
            elif c >= 97 and c <= 122:
                count_arr[c - 97] += 1;            # lowercase a-z
            elif (c >= 32 and c <= 126) or c == 9 or c == 10 or c == 13:
                ignored += 1;                  # numbers and punct, or TAB, CR, LF
            # else: ?
            # return inf?

        chi_squared = 0
        total_len = len(plaintext) - ignored
        for i in range(LETTERS_IN_ENGLISH):
            expected = total_len * english_freq[i]
            difference = count_arr[i] - expected
            if expected != 0:
                chi_squared += pow(difference , 2) / expected
                
        return chi_squared 


    def brute_force(self, cipher_text: bytes, key_length: int) -> str:
        """Breaks a Repeated Key Cipher by brute-forcing all keys."""
        
        # Generate keys.
        key_pos = [key for key in range(256)] # 2^8 possibilities for each byte.
        # We will generate cartesian product in the desired length.
        keys = [key for key in itertools.product(key_pos, repeat = key_length)] 

        highest_score = 0
        msg = cipher_text.decode()

        for key in keys:
            dec_text = RepeatedKeyCipher(bytes(key)).decrypt(cipher_text)
            score = self.plaintext_score(dec_text)
            if score > highest_score:
                highest_score = score
                msg = dec_text

        return msg

    def split_by_n(self, seq, n):
        '''A generator to divide a sequence into chunks of n units.'''
        while seq:
            yield seq[:n]
            seq = seq[n:]

    def smarter_break(self, cipher_text: bytes, key_length: int) -> str:
        """Breaks a Repeated Key Cipher any way you like."""
        
        ciphered_msg = bytearray(cipher_text).decode() #Get the ciphered message.
        number_of_partiotions = int(len(ciphered_msg) / key_length)
        split_msg = list(self.split_by_n(ciphered_msg, key_length))
        best_key = [0] * key_length

        return RepeatedKeyCipher(bytes(best_key)).decrypt(cipher_text)



