import zlib
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Counter

# generate random IV & Key
def read_IV_and_KEY():
    IV = Random.new().read(AES.block_size)
    KEY = Random.new().read(AES.block_size)
    return IV, KEY

# encrypt the message & compress it using zlib
def encrypt(msg):
    ctr = Counter.new(128)
    cipher = AES.new(KEY, AES.MODE_CTR, counter=ctr)
    return cipher.encrypt(zlib.compress(msg))

# encrypt_oracle: function used for encryption
# known: known prefix of secret
# special_sequence: sequence of special characters
# secret: the secret to be discovered
# max_len: max length of secret
# found_chars: list to store found chars of secret
def attack(encrypt_oracle, known, special_sequence, secret, max_len):
    found_chars = []
    
    # loop to guess next character (iterating through ASCII values 33 to 126)
    for i in range(33, 127):
        # encrypt + compress two different sequences
        # one with the guessed character before the special sequence and the other after
        enc1 = encrypt_oracle(known + bytes([i]) + special_sequence + b' ' + secret)
        enc2 = encrypt_oracle(known + special_sequence + bytes([i]) + b' ' + secret)
        
        # compression length - check which encryption is shorter, indicating a correct guess
        if len(enc1) < len(enc2):
            found_chars.append(bytes([i]))
    
    # recursive call & handling ambiguities 
    if len(found_chars) == 1:
        known += found_chars[0]
        if len(known) >= max_len:
            return known
        return attack(encrypt_oracle, known, special_sequence, secret, max_len)
    
    # if there are multiple chars that could potentially be the next char of the secret
    elif len(found_chars) > 1:
        print("Ambiguity detected. Choosing the most compressed one.")
        # the one char that results in the most compressed ciphertext is chosen
        # done by checking the length of the encrypted message for each character and picking 
        # one that results in the maximum compression
        max_compression_char = max(found_chars, key=lambda ch: len(encrypt_oracle(known + ch + special_sequence + b' ' + secret)))
        known += max_compression_char
        if len(known) >= max_len:
            return known
        # recursively call the attack function to continue discovering
        return attack(encrypt_oracle, known, special_sequence, secret, max_len)
    
    else:
        # end attack
        print("No further characters found.")
        return known

if __name__ == '__main__':
    IV, KEY = read_IV_and_KEY()

    SECRET = "GroupPassphrase=Secure123!".encode('utf-8')
    print("Secret TOKEN:", SECRET)

    # used to detect changes in the compressed and encrypted message
    SPECIAL_SEQUENCE = '~#:/[|/ç'.encode('utf-8')

    recovered_secret = attack(encrypt, b"GroupPassphrase=", SPECIAL_SEQUENCE, SECRET, len(SECRET))
    print("Recovered secret:", recovered_secret.decode('utf-8'))