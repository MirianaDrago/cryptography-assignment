from Crypto.Cipher import AES
from Crypto.Util import Counter

key = b'Sixteen byte key'
initial_ctr_value = 1

# one known plaintext
known_plaintext = b'Known plaintext 1'

# encrypting the known plaintext with a repeating keystream
ctr = Counter.new(128, initial_value=initial_ctr_value)
cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
ciphertext = cipher.encrypt(known_plaintext)

# calculating the keystream by XORing the known plaintext with the corresponding ciphertext
# keystream is the sequence of bytes that was used to encrypt the known plaintext, determined by key and counter value
keystream = bytes([p ^ c for p, c in zip(known_plaintext, ciphertext)])
print("Keystream: ", keystream)

# encrypting another plaintext with the same keystream
another_plaintext = b'Known plaintext 2'
ctr = Counter.new(128, initial_value=initial_ctr_value) # same initial value for repeating keystream
cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
other_ciphertext = cipher.encrypt(another_plaintext)

# decrypt using the keystream - XORING ciphertext with keystream -> giving back original plaintext
decrypted_text = bytes([c ^ k for c, k in zip(other_ciphertext, keystream)])

# validating the attack
if decrypted_text == another_plaintext:
    print("Attack successful!")
else:
    print("Attack failed!")

print("Decrypted text:", decrypted_text.decode())
