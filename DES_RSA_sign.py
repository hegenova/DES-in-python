import socket
import threading
import sys
import random
import json
import base64
import hashlib

# ==================== DES Implementation ====================
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

P = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

S_BOXES = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

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
    key_bits = string_to_bits(key)
    key_56 = permute(key_bits, PC1)
    C = key_56[:28]
    D = key_56[28:]
    subkeys = []
    for round_num in range(16):
        C = left_shift(C, SHIFT_SCHEDULE[round_num])
        D = left_shift(D, SHIFT_SCHEDULE[round_num])
        CD = C + D
        subkey = permute(CD, PC2)
        subkeys.append(subkey)
    return subkeys

def f_function(right, subkey):
    expanded = permute(right, E)
    xored = xor(expanded, subkey)
    s_output = []
    for i in range(8):
        block = xored[i * 6:(i + 1) * 6]
        s_output.extend(s_box_lookup(block, S_BOXES[i]))
    result = permute(s_output, P)
    return result

def des_cipher(block, subkeys):
    block = permute(block, IP)
    left = block[:32]
    right = block[32:]
    for subkey in subkeys:
        temp = right
        right = xor(left, f_function(right, subkey))
        left = temp
    combined = right + left
    result = permute(combined, FP)
    return result

def pad_text(text):
    padding_length = 8 - (len(text) % 8)
    padding = chr(padding_length) * padding_length
    return text + padding

def unpad_text(text):
    padding_length = ord(text[-1])
    return text[:-padding_length]

def des_encrypt(plaintext, key):
    if len(key) < 8:
        key = key.ljust(8, '\x00')
    elif len(key) > 8:
        key = key[:8]
    plaintext = pad_text(plaintext)
    subkeys = generate_subkeys(key)
    ciphertext = []
    for i in range(0, len(plaintext), 8):
        block = plaintext[i:i + 8]
        block_bits = string_to_bits(block)
        encrypted_bits = des_cipher(block_bits, subkeys)
        ciphertext.extend(encrypted_bits)
    return bits_to_string(ciphertext)

def des_decrypt(ciphertext, key):
    if len(key) < 8:
        key = key.ljust(8, '\x00')
    elif len(key) > 8:
        key = key[:8]
    subkeys = generate_subkeys(key)
    subkeys = subkeys[::-1]
    plaintext = []
    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i + 8]
        block_bits = string_to_bits(block)
        decrypted_bits = des_cipher(block_bits, subkeys)
        plaintext.extend(decrypted_bits)
    plaintext_str = bits_to_string(plaintext)
    return unpad_text(plaintext_str)

# ==================== RSA Implementation ====================

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def mod_inverse(e, phi):
    gcd_val, x, _ = extended_gcd(e, phi)
    if gcd_val != 1:
        return None
    return (x % phi + phi) % phi

def is_prime(n, k=5):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits=64):
    """Generate a prime number with specified bit length"""
    while True:
        num = random.randrange(2**(bits-1), 2**bits)
        if is_prime(num):
            return num

def generate_rsa_keypair(bits=64):
    """Generate RSA keypair with larger key size to handle 8-char strings"""
    p = generate_prime(bits)
    q = generate_prime(bits)
    while p == q:
        q = generate_prime(bits)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537
    if e >= phi or gcd(e, phi) != 1:
        e = 3
        while gcd(e, phi) != 1:
            e += 2
    
    d = mod_inverse(e, phi)
    
    return (e, n), (d, n)

def rsa_encrypt(message, public_key):
    e, n = public_key
    return pow(message, e, n)

def rsa_decrypt(ciphertext, private_key):
    d, n = private_key
    return pow(ciphertext, d, n)

def string_to_int(s):
    """Convert string to integer for RSA encryption using base64"""
    string_bytes = s.encode('ascii')
    return int.from_bytes(string_bytes, byteorder='big')

def int_to_string(num):
    """Convert integer back to string after RSA decryption"""
    num_bytes = (num.bit_length() + 7) // 8
    string_bytes = num.to_bytes(num_bytes, byteorder='big')
    return string_bytes.decode('ascii')

# ==================== DIGITAL SIGNATURE Implementation ====================
# Implementasi sistem Public Key Cryptosystems untuk Digital Signature

def simple_hash(message):
    """
    Membuat hash dari pesan menggunakan SHA-256
    Hash digunakan untuk membuat digest yang akan ditandatangani
    """
    # Menggunakan SHA-256 untuk membuat hash
    hash_obj = hashlib.sha256(message.encode('utf-8'))
    # Konversi hash ke integer untuk operasi RSA
    hash_int = int(hash_obj.hexdigest(), 16)
    return hash_int

def create_signature(message, private_key):
    """
    Membuat digital signature dari pesan
    
    Proses:
    1. Buat hash dari pesan (message digest)
    2. Enkripsi hash dengan private key pengirim
    
    Args:
        message: Pesan yang akan ditandatangani
        private_key: Private key pengirim (d, n)
    
    Returns:
        signature: Tanda tangan digital (integer)
    """
    d, n = private_key
    # Step 1: Hash pesan
    message_hash = simple_hash(message)
    # Step 2: Modulo hash agar tidak melebihi n
    message_hash = message_hash % n
    # Step 3: "Enkripsi" hash dengan private key (Sign)
    # Signature = hash^d mod n
    signature = pow(message_hash, d, n)
    return signature

def verify_signature(message, signature, public_key):
    """
    Memverifikasi digital signature
    
    Proses:
    1. Dekripsi signature dengan public key pengirim
    2. Buat hash dari pesan yang diterima
    3. Bandingkan kedua hash
    
    Args:
        message: Pesan yang diterima
        signature: Tanda tangan digital
        public_key: Public key pengirim (e, n)
    
    Returns:
        bool: True jika signature valid, False jika tidak
    """
    e, n = public_key
    # Step 1: "Dekripsi" signature dengan public key
    # Decrypted = signature^e mod n
    decrypted_hash = pow(signature, e, n)
    # Step 2: Hash pesan yang diterima
    message_hash = simple_hash(message)
    message_hash = message_hash % n
    # Step 3: Bandingkan
    return decrypted_hash == message_hash

# ==================== Network Utilities ====================

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def generate_random_des_key():
    """Generate random 8-character DES key (alphanumeric only for safety)"""
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(chars) for _ in range(8))

DEFAULT_PORT = 5555

# ==================== Device Classes ====================

class Device:
    def __init__(self, device_name):
        self.device_name = device_name
        self.key = None  # DES key for encryption
        self.running = True
        self.socket = None
        self.key_exchanged = False
        # Digital Signature keys
        self.my_public_key = None      # Public key milik sendiri
        self.my_private_key = None     # Private key milik sendiri
        self.peer_public_key = None    # Public key milik peer (untuk verifikasi signature)
    
    def receive_messages(self, conn):
        while self.running:
            try:
                data = conn.recv(8192)
                if not data:
                    print("\n✗ Connection lost!")
                    self.running = False
                    break
                
                # Parse received data (JSON format dengan encrypted message + signature)
                received_json = json.loads(data.decode('utf-8'))
                encrypted_msg_b64 = received_json['encrypted_message']
                signature = int(received_json['signature'])
                
                # Decode dari base64
                encrypted_msg = base64.b64decode(encrypted_msg_b64).decode('latin-1')
                
                # Show encrypted message
                print(f"\n[Encrypted]: {repr(encrypted_msg[:50])}...")
                print(f"[Signature]: {signature}")
                
                # Decrypt message dengan DES
                decrypted_msg = des_decrypt(encrypted_msg, self.key)
                
                # Verify signature dengan public key peer
                is_valid = verify_signature(decrypted_msg, signature, self.peer_public_key)
                
                if is_valid:
                    print(f"[✓ Signature VALID - Message authenticated]")
                else:
                    print(f"[✗ Signature INVALID - Message may be tampered!]")
                
                if decrypted_msg.lower() == 'quit':
                    print("\n✗ Other device has left the chat.")
                    self.running = False
                    break
                
                status = "✓" if is_valid else "⚠"
                print(f"[Other Device] {status}: {decrypted_msg}")
                print("You: ", end='', flush=True)
            except json.JSONDecodeError as e:
                if self.running:
                    print(f"\n✗ Error parsing message: {e}")
                break
            except Exception as e:
                if self.running:
                    print(f"\n✗ Error receiving: {e}")
                    import traceback
                    traceback.print_exc()
                break
    
    def send_messages(self, conn):
        while self.running:
            try:
                message = input("You: ")
                
                if not message.strip():
                    continue
                
                # Encrypt message dengan DES
                encrypted_msg = des_encrypt(message, self.key)
                
                # Create digital signature dengan private key sendiri
                signature = create_signature(message, self.my_private_key)
                
                # Encode encrypted message ke base64 untuk JSON
                encrypted_msg_b64 = base64.b64encode(encrypted_msg.encode('latin-1')).decode('utf-8')
                
                # Pack ke JSON
                send_data = json.dumps({
                    'encrypted_message': encrypted_msg_b64,
                    'signature': str(signature)
                })
                
                print(f"[Sending encrypted]: {repr(encrypted_msg[:50].encode('latin-1'))}...")
                print(f"[Signature created]: {signature}")
                
                conn.send(send_data.encode('utf-8'))
                
                if message.lower() == 'quit':
                    print("✓ Disconnecting...")
                    self.running = False
                    break
                
            except KeyboardInterrupt:
                print("\n✗ Interrupted by user")
                self.running = False
                break
            except Exception as e:
                if self.running:
                    print(f"✗ Error sending: {e}")
                    import traceback
                    traceback.print_exc()
                break


class ServerDevice(Device):
    def __init__(self, port=DEFAULT_PORT):
        super().__init__("Server Device")
        self.port = port
        self.host = '0.0.0.0'
        self.server_rsa_public = None   # RSA untuk key exchange
        self.server_rsa_private = None  # RSA untuk key exchange
    
    def perform_key_exchange(self, client_socket):
        print("\n" + "=" * 70)
        print("  RSA KEY EXCHANGE & SIGNATURE KEY DISTRIBUTION")
        print("=" * 70)
        
        # Step 1: Generate RSA keypair untuk key exchange
        print("\n[1/6] Generating RSA keypair for KEY EXCHANGE (64-bit primes)...")
        self.server_rsa_public, self.server_rsa_private = generate_rsa_keypair(bits=64)
        e, n = self.server_rsa_public
        print(f"      ✓ Key Exchange Public Key: (e={e}, n={n})")
        
        # Step 2: Generate RSA keypair untuk DIGITAL SIGNATURE
        print("\n[2/6] Generating RSA keypair for DIGITAL SIGNATURE (64-bit primes)...")
        self.my_public_key, self.my_private_key = generate_rsa_keypair(bits=64)
        sig_e, sig_n = self.my_public_key
        print(f"      ✓ Signature Public Key: (e={sig_e}, n={sig_n})")
        print(f"      ✓ Signature Private Key: [KEPT SECRET]")
        
        # Step 3: Send public keys to client (key exchange + signature verification)
        print("\n[3/6] Sending public keys to Client...")
        public_key_data = json.dumps({
            'key_exchange': {'e': e, 'n': n},
            'signature': {'e': sig_e, 'n': sig_n}
        })
        client_socket.send(public_key_data.encode())
        print("      ✓ Key Exchange Public Key sent")
        print("      ✓ Signature Public Key sent (for client to verify server's messages)")
        
        # Step 4: Receive encrypted DES key AND client's signature public key
        print("\n[4/6] Waiting for encrypted DES key & Client's signature public key...")
        received_data = client_socket.recv(8192).decode()
        received_json = json.loads(received_data)
        
        encrypted_key_int = int(received_json['encrypted_des_key'])
        client_sig_public = received_json['signature_public_key']
        self.peer_public_key = (client_sig_public['e'], client_sig_public['n'])
        
        print(f"      ✓ Received encrypted DES key (int): {encrypted_key_int}")
        print(f"      ✓ Received Client's Signature Public Key: (e={client_sig_public['e']}, n={client_sig_public['n']})")
        
        # Step 5: Decrypt DES key with private key
        print("\n[5/6] Decrypting DES key with RSA private key...")
        decrypted_key_int = rsa_decrypt(encrypted_key_int, self.server_rsa_private)
        self.key = int_to_string(decrypted_key_int)
        print(f"      ✓ Decrypted DES Key: '{self.key}'")
        
        # Step 6: Send confirmation
        print("\n[6/6] Sending key exchange confirmation...")
        client_socket.send(b"KEY_EXCHANGE_COMPLETE")
        
        print("\n" + "=" * 70)
        print("  ✓ KEY EXCHANGE & SIGNATURE SETUP SUCCESSFUL!")
        print("=" * 70)
        print(f"  Shared DES Key: '{self.key}'")
        print(f"  Server Signature Key: [PRIVATE - for signing outgoing messages]")
        print(f"  Client Signature Key: [PUBLIC - for verifying incoming messages]")
        print("=" * 70)
        print("\n  SECURITY FEATURES:")
        print("  • Messages encrypted with DES (confidentiality)")
        print("  • Messages signed with RSA (authentication & integrity)")
        print("  • Signature verification ensures message authenticity")
        print("=" * 70)
        
        self.key_exchanged = True
    
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)
        except Exception as e:
            print(f"✗ Failed to start server: {e}")
            return
        
        local_ip = get_local_ip()
        
        print("\n" + "=" * 70)
        print("  DEVICE 1 - SERVER MODE (DES + RSA + DIGITAL SIGNATURE)")
        print("=" * 70)
        print(f"  Server IP: {local_ip}")
        print(f"  Port: {self.port}")
        print("\n  ⚠ IMPORTANT: Tell Device 2 to connect to: {local_ip}")
        print("\n  Waiting for Device 2 to connect...")
        print("=" * 70)
        
        try:
            client_socket, address = server_socket.accept()
            print(f"\n✓ Device 2 connected from {address[0]}:{address[1]}")
            
            # Perform key exchange & signature setup
            self.perform_key_exchange(client_socket)
            
            # Start chat
            print("\n  Chat started! Type your message and press Enter.")
            print("  All messages are encrypted AND signed for security.")
            print("  Type 'quit' to exit.\n")
            
            receive_thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
            receive_thread.daemon = True
            receive_thread.start()
            
            self.send_messages(client_socket)
            
            client_socket.close()
        except KeyboardInterrupt:
            print("\n✗ Server stopped by user")
        finally:
            server_socket.close()


class ClientDevice(Device):
    def __init__(self, server_ip, port=DEFAULT_PORT):
        super().__init__("Client Device")
        self.server_ip = server_ip
        self.port = port
    
    def perform_key_exchange(self, client_socket):
        print("\n" + "=" * 70)
        print("  RSA KEY EXCHANGE & SIGNATURE KEY DISTRIBUTION")
        print("=" * 70)
        
        # Step 1: Receive public keys from server
        print("\n[1/6] Waiting for Server's public keys...")
        public_key_data = client_socket.recv(8192).decode()
        public_key_dict = json.loads(public_key_data)
        
        # Key exchange public key
        server_ke_public = public_key_dict['key_exchange']
        server_key_exchange_key = (server_ke_public['e'], server_ke_public['n'])
        
        # Server's signature public key (untuk verifikasi pesan dari server)
        server_sig_public = public_key_dict['signature']
        self.peer_public_key = (server_sig_public['e'], server_sig_public['n'])
        
        print(f"      ✓ Key Exchange Public Key: (e={server_ke_public['e']}, n={server_ke_public['n']})")
        print(f"      ✓ Server's Signature Public Key: (e={server_sig_public['e']}, n={server_sig_public['n']})")
        
        # Step 2: Generate random DES key
        print("\n[2/6] Generating random DES key...")
        self.key = generate_random_des_key()
        print(f"      ✓ Generated DES Key: '{self.key}'")
        
        # Step 3: Generate RSA keypair untuk DIGITAL SIGNATURE
        print("\n[3/6] Generating RSA keypair for DIGITAL SIGNATURE (64-bit primes)...")
        self.my_public_key, self.my_private_key = generate_rsa_keypair(bits=64)
        sig_e, sig_n = self.my_public_key
        print(f"      ✓ Signature Public Key: (e={sig_e}, n={sig_n})")
        print(f"      ✓ Signature Private Key: [KEPT SECRET]")
        
        # Step 4: Encrypt DES key with server's key exchange public key
        print("\n[4/6] Encrypting DES key with Server's public key...")
        key_int = string_to_int(self.key)
        encrypted_key = rsa_encrypt(key_int, server_key_exchange_key)
        print(f"      ✓ Encrypted DES key (int): {encrypted_key}")
        
        # Step 5: Send encrypted DES key AND client's signature public key
        print("\n[5/6] Sending encrypted DES key & Signature public key to Server...")
        send_data = json.dumps({
            'encrypted_des_key': str(encrypted_key),
            'signature_public_key': {'e': sig_e, 'n': sig_n}
        })
        client_socket.send(send_data.encode())
        print("      ✓ Encrypted DES key sent")
        print("      ✓ Signature Public Key sent (for server to verify client's messages)")
        
        # Step 6: Wait for confirmation
        print("\n[6/6] Waiting for key exchange confirmation...")
        confirmation = client_socket.recv(1024).decode()
        if confirmation == "KEY_EXCHANGE_COMPLETE":
            print("      ✓ Key exchange confirmed by Server")
        
        print("\n" + "=" * 70)
        print("  ✓ KEY EXCHANGE & SIGNATURE SETUP SUCCESSFUL!")
        print("=" * 70)
        print(f"  Shared DES Key: '{self.key}'")
        print(f"  Client Signature Key: [PRIVATE - for signing outgoing messages]")
        print(f"  Server Signature Key: [PUBLIC - for verifying incoming messages]")
        print("=" * 70)
        print("\n  SECURITY FEATURES:")
        print("  • Messages encrypted with DES (confidentiality)")
        print("  • Messages signed with RSA (authentication & integrity)")
        print("  • Signature verification ensures message authenticity")
        print("=" * 70)
        
        self.key_exchanged = True
    
    def start(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print("\n" + "=" * 70)
        print("  DEVICE 2 - CLIENT MODE (DES + RSA + DIGITAL SIGNATURE)")
        print("=" * 70)
        print(f"  Connecting to Server: {self.server_ip}:{self.port}")
        print("=" * 70)
        
        try:
            client_socket.connect((self.server_ip, self.port))
            print("\n✓ Connected to Device 1!")
            
            # Perform key exchange & signature setup
            self.perform_key_exchange(client_socket)
            
            # Start chat
            print("\n  Chat started! Type your message and press Enter.")
            print("  All messages are encrypted AND signed for security.")
            print("  Type 'quit' to exit.\n")
            
            receive_thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
            receive_thread.daemon = True
            receive_thread.start()
            
            self.send_messages(client_socket)
            
        except Exception as e:
            print(f"\n✗ Connection failed: {e}")
            print("\n  Tips:")
            print("    1. Make sure Device 1 is running (server mode)")
            print("    2. Check the IP address is correct")
            print("    3. Ensure both devices are on the same network")
            print("    4. Check firewall (port 5555 might be blocked)")
        finally:
            client_socket.close()


def main():
    print("\n" + "=" * 70)
    print("  DES ENCRYPTED CHAT WITH RSA KEY DISTRIBUTION")
    print("  + DIGITAL SIGNATURE (PUBLIC KEY CRYPTOSYSTEMS)")
    print("=" * 70)
    print("\n  Security Protocol:")
    print("  ┌─────────────────────────────────────────────────────────────┐")
    print("  │  KEY EXCHANGE (RSA):                                        │")
    print("  │  1. Server generates RSA keypair for key exchange           │")
    print("  │  2. Server sends public key to Client                       │")
    print("  │  3. Client generates random DES key                         │")
    print("  │  4. Client encrypts DES key with RSA public key             │")
    print("  │  5. Server decrypts DES key with RSA private key            │")
    print("  ├─────────────────────────────────────────────────────────────┤")
    print("  │  DIGITAL SIGNATURE (RSA):                                   │")
    print("  │  1. Both devices generate their own RSA keypair             │")
    print("  │  2. Public keys exchanged for signature verification        │")
    print("  │  3. Sender signs message hash with PRIVATE key              │")
    print("  │  4. Receiver verifies signature with sender's PUBLIC key    │")
    print("  ├─────────────────────────────────────────────────────────────┤")
    print("  │  MESSAGE SECURITY:                                          │")
    print("  │  • Confidentiality: DES encryption                          │")
    print("  │  • Authentication: RSA digital signature                    │")
    print("  │  • Integrity: Hash verification via signature               │")
    print("  └─────────────────────────────────────────────────────────────┘")
    print("=" * 70)
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        print("\nChoose mode:")
        print("1. Device 1 (Server) - Wait for connection")
        print("2. Device 2 (Client) - Connect to server")
        print("=" * 70)
        mode = input("\nEnter choice (1/2): ").strip()
    
    if mode == '1':
        server = ServerDevice(port=DEFAULT_PORT)
        server.start()
    elif mode == '2':
        if len(sys.argv) > 2:
            server_ip = sys.argv[2]
        else:
            server_ip = input("\nEnter Device 1 (Server) IP address: ").strip()
        
        if not server_ip:
            print("✗ IP address cannot be empty!")
            return
        
        client = ClientDevice(server_ip, port=DEFAULT_PORT)
        client.start()
    else:
        print("✗ Invalid choice!")


if __name__ == "__main__":
    main()