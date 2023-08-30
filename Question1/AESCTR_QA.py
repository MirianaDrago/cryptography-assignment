from Crypto.Cipher import AES
from Crypto.Util import Counter as CryptoCounter
from collections import defaultdict

key = b'Sixteen byte key'
initial_ctr_value = 22

plaintexts = [
    b'from: Miriana Drago\r\nsecret: group_passphrase\r\nto: Prof. Smith\r\nmsg: Can I meet you tomorrow?',
    b'from: Roberto Drago\r\nsecret: group_passphrase\r\nto: Math Dept.\r\nmsg: I will submit by Friday.',
    b'from: Simone Drago\r\nsecret: group_passphrase\r\nto: Dr. Jones\r\nmsg: I need a prescription.',
    b'from: Nicole Drago\r\nsecret: group_passphrase\r\nto: Dr. Jones\r\nmsg: I need a refill for my prescription.'
]

# function to perform frequency analysis
def frequency_analysis(ciphertexts):
    # dictionary to store byte frequencies
    byte_frequencies = defaultdict(int)
    for ciphertext in ciphertexts:
        # loop through each byte in the ciphertext
        for byte in ciphertext:
            # increment frequency count for each byte
            byte_frequencies[byte] += 1
    return byte_frequencies

# encrypt plain texts using AES-CTR with a repeating key stream
ciphertexts_repeating = []
for plaintext in plaintexts: 
    ctr = CryptoCounter.new(128, initial_value=initial_ctr_value)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    ciphertexts_repeating.append(cipher.encrypt(plaintext))

# encrypt plain texts using AES-CTR with a non-repeating key stream
ciphertexts_non_repeating = []
for i, plaintext in enumerate(plaintexts): 
    ctr = CryptoCounter.new(128, initial_value=initial_ctr_value + i)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    ciphertexts_non_repeating.append(cipher.encrypt(plaintext))

# frequency analysis
freq_repeating = frequency_analysis(ciphertexts_repeating)
freq_non_repeating = frequency_analysis(ciphertexts_non_repeating)

# results
print("Frequency analysis with repeating keystream:")
# 10 most common bytes
for byte, freq in sorted(freq_repeating.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"Byte: {byte}, Frequency: {freq}")

print("\nFrequency analysis with non-repeating keystream:")
for byte, freq in sorted(freq_non_repeating.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"Byte: {byte}, Frequency: {freq}")

# assuming the most common plaintext byte is for 'f' (ASCII 102)
# this is just a test
known_plaintext_byte = 102

# the most common ciphertext byte from the frequency analysis
most_common_ciphertext_byte = max(freq_repeating, key=freq_repeating.get)

# guess the key stream byte
guessed_keystream_byte = most_common_ciphertext_byte ^ known_plaintext_byte
print(f"Guessed key stream byte for 'f': {guessed_keystream_byte}")

# decrypt occurrences of the most common ciphertext byte
for i, ciphertext in enumerate(ciphertexts_repeating):
    decrypted_bytes = [b ^ guessed_keystream_byte if b == most_common_ciphertext_byte else None for b in ciphertext]
    decrypted_chars = [chr(b) for b in decrypted_bytes if b is not None]
    print(f"Decrypted occurrences in ciphertext {i+1}: {decrypted_chars}")