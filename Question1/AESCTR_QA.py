from Crypto.Cipher import AES
from Crypto.Util import Counter as CryptoCounter
from collections import Counter as CollectionsCounter

key = b'Sixteen byte key'
initial_ctr_value = 22
initial_nr_ctr_value = 1

plaintexts = [
    b'My name is Miriana Drago, I am 23 years old and I study Computer Science.',
    b'My name is Roberto Drago, I am 18 years old and I study Mathematics.',
    b'My name is Simone Drago, I am 50 years old and I study Medicine.'
]

ciphertexts = []
non_repeating_ciphertexts = []

# repeating key stream

for plaintext in plaintexts: 
    ctr = CryptoCounter.new(128, initial_valuesho=initial_ctr_value) # same initial value for each plaintext
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    ciphertext = cipher.encrypt(plaintext)
    ciphertexts.append(ciphertext)

# frequency analysis attack on repeating keystream

# combine all ciphertexts into one bytearray
combined_ciphertext = b''.join(ciphertexts)
# count the frequency of each byte value in the combined ciphertext
byte_frequencies = CollectionsCounter(combined_ciphertext)
# print the most common byte values and their frequencies
print("REPEATING KEYSTREAM")
for byte_value, frequency in byte_frequencies.most_common():
    print(f"Byte value: {byte_value}, Frequency: {frequency}")

# non-repeating key stream

ctr = CryptoCounter.new(128, initial_value=initial_nr_ctr_value)
cipher = AES.new(key, AES.MODE_CTR, counter=ctr)

for plaintext in plaintexts:
    ciphertext = cipher.encrypt(plaintext)
    non_repeating_ciphertexts.append(ciphertext)

# frequency analysis attack on non-repeating keystream

# combine all ciphertexts into one bytearray
combined_nr_ciphertext = b''.join(non_repeating_ciphertexts)
# count the frequency of each byte value in the combined ciphertext
byte_nr_frequencies = CollectionsCounter(combined_nr_ciphertext)
# print the most common byte values and their frequencies
print("NON-REPEATING KEYSTREAM")
for byte_value, frequency in byte_nr_frequencies.most_common():
    print(f"Byte value: {byte_value}, Frequency: {frequency}")