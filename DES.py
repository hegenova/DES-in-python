
# Initial Permutation Table
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Final Permutation Table (Inverse of IP)
FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

# Expansion Table (32 bits to 48 bits)
E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

# Permutation Table after S-box substitution
P = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

# S-boxes (Substitution boxes)
S_BOXES = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

# Permuted Choice 1 (PC1) - selects 56 bits from 64-bit key
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# Permuted Choice 2 (PC2) - selects 48 bits from 56-bit key
PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Number of left shifts for each round
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


def string_to_bits(text):
    bits = []
    for char in text:
        byte = ord(char)
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits


def bits_to_string(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bits):
                byte = (byte << 1) | bits[i + j]
        chars.append(chr(byte))
    return ''.join(chars)


def permute(block, table):
    return [block[i - 1] for i in table]


def xor(bits1, bits2):
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]


def left_shift(bits, n):
    return bits[n:] + bits[:n]


def s_box_lookup(block, s_box):
    row = (block[0] << 1) | block[5]
    col = (block[1] << 3) | (block[2] << 2) | (block[3] << 1) | block[4]
    value = s_box[row][col]
    return [(value >> i) & 1 for i in range(3, -1, -1)]


def generate_subkeys(key):
    # Convert key to bits
    key_bits = string_to_bits(key)
    
    # Apply PC1 to get 56-bit key
    key_56 = permute(key_bits, PC1)
    
    # Split into left and right halves
    C = key_56[:28]
    D = key_56[28:]
    
    subkeys = []
    for round_num in range(16):
        # Perform left shifts
        C = left_shift(C, SHIFT_SCHEDULE[round_num])
        D = left_shift(D, SHIFT_SCHEDULE[round_num])
        
        # Combine and apply PC2 to get 48-bit subkey
        CD = C + D
        subkey = permute(CD, PC2)
        subkeys.append(subkey)
    
    return subkeys


def f_function(right, subkey):
    # Expansion: 32 bits to 48 bits
    expanded = permute(right, E)
    
    # XOR with subkey
    xored = xor(expanded, subkey)
    
    # S-box substitution: 48 bits to 32 bits
    s_output = []
    for i in range(8):
        block = xored[i * 6:(i + 1) * 6]
        s_output.extend(s_box_lookup(block, S_BOXES[i]))
    
    # Permutation
    result = permute(s_output, P)
    
    return result


def des_cipher(block, subkeys):
    # Initial permutation
    block = permute(block, IP)
    
    # Split into left and right halves
    left = block[:32]
    right = block[32:]
    
    # 16 rounds of Feistel network
    for subkey in subkeys:
        temp = right
        right = xor(left, f_function(right, subkey))
        left = temp
    
    # Swap left and right (no swap on last round, so we swap here)
    combined = right + left
    
    # Final permutation
    result = permute(combined, FP)
    
    return result


def pad_text(text):
    """Pad text to multiple of 8 bytes using PKCS7 padding"""
    padding_length = 8 - (len(text) % 8)
    padding = chr(padding_length) * padding_length
    return text + padding


def unpad_text(text):
    """Remove PKCS7 padding"""
    padding_length = ord(text[-1])
    return text[:-padding_length]


def des_encrypt(plaintext, key):
    """Encrypt plaintext using DES"""
    # Ensure key is 8 bytes
    if len(key) < 8:
        key = key.ljust(8, '\x00')
    elif len(key) > 8:
        key = key[:8]
    
    # Pad plaintext
    plaintext = pad_text(plaintext)
    
    # Generate subkeys
    subkeys = generate_subkeys(key)
    
    # Encrypt each 8-byte block
    ciphertext = []
    for i in range(0, len(plaintext), 8):
        block = plaintext[i:i + 8]
        block_bits = string_to_bits(block)
        encrypted_bits = des_cipher(block_bits, subkeys)
        ciphertext.extend(encrypted_bits)
    
    return bits_to_string(ciphertext)


def des_decrypt(ciphertext, key):
    """Decrypt ciphertext using DES"""
    # Ensure key is 8 bytes
    if len(key) < 8:
        key = key.ljust(8, '\x00')
    elif len(key) > 8:
        key = key[:8]
    
    # Generate subkeys (reversed for decryption)
    subkeys = generate_subkeys(key)
    subkeys = subkeys[::-1]
    
    # Decrypt each 8-byte block
    plaintext = []
    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i + 8]
        block_bits = string_to_bits(block)
        decrypted_bits = des_cipher(block_bits, subkeys)
        plaintext.extend(decrypted_bits)
    
    plaintext_str = bits_to_string(plaintext)
    return unpad_text(plaintext_str)


if __name__ == "__main__":
    key = "abcdefgh"  # 8-byte key
    plaintext = "Tes DES Encryption"
    
    print("Original plaintext:", plaintext)
    print("Key:", key)
    print()
    
    # Encrypt
    encrypted = des_encrypt(plaintext, key)
    print("Encrypted (hex):", encrypted.encode('latin-1').hex())
    print()
    
    # Decrypt
    decrypted = des_decrypt(encrypted, key)
    print("Decrypted plaintext:", decrypted)
    print()
    
    # Verify
    if plaintext == decrypted:
        print("Encryption and decryption successful")
    else:
        print("Error in encryption/decryption")