from Crypto.Cipher import AES
from Crypto.Util import Counter
import zlib

def attack(encrypt_oracle, known_prefix, padding_byte):
    """
    Recovers a secret using the CRIME attack (CTR version).
    :param encrypt_oracle: the encryption oracle
    :param known_prefix: a known prefix of the secret to recover
    :param padding_byte: a byte which is never used in the plaintext
    :return: the secret
    """
    known_prefix = bytearray(known_prefix) # a portion of the plaintext that the attacker already knows or can guess
    padding_bytes = bytes([padding_byte])
    while True:
        for i in range(256):
            # Don't try the padding byte.
            if i == padding_byte:
                continue

            l1 = len(encrypt_oracle(padding_bytes + known_prefix + bytes([i]) + padding_bytes + padding_bytes))
            l2 = len(encrypt_oracle(padding_bytes + known_prefix + padding_bytes + bytes([i]) + padding_bytes))
            if l1 < l2:
                known_prefix.append(i)
                break
        else:
            return known_prefix

# encryption oracle compresses and then encrypts the plaintext using AES-CTR - returns the resulting ciphertext
def encrypt_oracle(plaintext):
    # key and initial counter value for AES-CTR
    key = b'Sixteen byte key'
    initial_ctr_value = 1

    # compressing the plaintext using DEFLATE
    compressed_plaintext = zlib.compress(plaintext)

    # encrypting the compressed plaintext using AES-CTR
    ctr = Counter.new(128, initial_value=initial_ctr_value)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    ciphertext = cipher.encrypt(compressed_plaintext)

    return ciphertext

# known prefix for the attack
known_prefix = b'from: someone\r\n'
# padding byte that is never used in the plaintext
padding_byte = 255
# secret to be recovered (for demonstration purposes)
secret = b'secret: passphrase\r\nto: another\r\nmsg: blablabla\r\n\r\n'
# full plaintext including the known prefix and the secret
plaintext = known_prefix + secret
# encryption oracle function that takes plaintext and returns ciphertext
oracle = lambda plaintext: encrypt_oracle(plaintext)
# executing the attack to recover the secret
recovered_secret = attack(oracle, known_prefix, padding_byte)
# print the recovered secret
print("Recovered secret:", recovered_secret.decode())