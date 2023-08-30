from Crypto.Cipher import AES
from Crypto.Util import Counter as CryptoCounter

key = b'Sixteen byte key'
initial_ctr_value = 22

plaintexts = [
    b'from: Miriana Drago\r\nsecret: group_passphrase\r\nto: Prof. Smith\r\nmsg: Can I meet you tomorrow?',
    b'from: Roberto Drago\r\nsecret: group_passphrase\r\nto: Math Dept.\r\nmsg: I will submit by Friday.',
]

ciphertexts = []

# encrypt with repeating key stream
for plaintext in plaintexts: 
    ctr = CryptoCounter.new(128, initial_value=initial_ctr_value) # same initial value for each plaintext
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    ciphertext = cipher.encrypt(plaintext)
    ciphertexts.append(ciphertext)

# known plaintext recovery
# if we know the plaintext for the first ciphertext, we can recover the key stream
known_plaintext = plaintexts[0]
# XOR the known plaintext with the ciphertext, giving the key stream
recovered_keystream = bytes([a ^ b for a, b in zip(known_plaintext, ciphertexts[0])])
# use the recovered key stream to decrypt the second ciphertext
recovered_plaintext = bytes([a ^ b for a, b in zip(recovered_keystream, ciphertexts[1])])

print("Known plaintext attack result: ", recovered_plaintext.decode('utf-8'))
