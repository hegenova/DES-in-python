"""
DES Encrypted Communication System - 2 Different Devices
Tugas: Komunikasi 2 device berbeda dengan enkripsi DES

CARA SETUP:
1. Install Python di kedua device
2. Pastikan kedua device dalam 1 network (WiFi/LAN sama)
3. Cari IP address Device 1 (yang jadi server)
4. Jalankan server di Device 1, client di Device 2
"""

import socket
import threading
import sys

# ==================== DES IMPLEMENTATION ====================

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

# ==================== NETWORK UTILITIES ====================

def get_local_ip():
    """Get local IP address of this device"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# ==================== DEVICE COMMUNICATION ====================

# Shared key (KEDUA DEVICE HARUS TAHU KEY INI!)
SHARED_KEY = "secret99"
DEFAULT_PORT = 5555

class Device:
    """Generic device class untuk server dan client"""
    def __init__(self, device_name, key=SHARED_KEY):
        self.device_name = device_name
        self.key = key
        self.running = True
        self.socket = None
    
    def receive_messages(self, conn):
        """Thread untuk menerima pesan"""
        while self.running:
            try:
                encrypted_msg = conn.recv(4096)
                if not encrypted_msg:
                    print("\n Connection lost!")
                    self.running = False
                    break
                
                # Decrypt pesan
                decrypted_msg = des_decrypt(encrypted_msg.decode('latin-1'), self.key)
                
                if decrypted_msg.lower() == 'quit':
                    print("\n Other device has left the chat.")
                    self.running = False
                    break
                
                print(f"\nOther Device: {decrypted_msg}")
                print(f"\nEncrypted Message: {encrypted_msg}")
                print("You: ", end='', flush=True)
            except Exception as e:
                if self.running:
                    print(f"\n Error receiving: {e}")
                break
    
    def send_messages(self, conn):
        """Main thread untuk mengirim pesan"""
        while self.running:
            try:
                message = input("You: ")
                
                if message.lower() == 'quit':
                    encrypted_msg = des_encrypt(message, self.key)
                    conn.send(encrypted_msg.encode('latin-1'))
                    print(" Disconnecting...")
                    self.running = False
                    break
                
                if not message.strip():
                    continue
                
                # Encrypt dan kirim
                encrypted_msg = des_encrypt(message, self.key)
                conn.send(encrypted_msg.encode('latin-1'))
                
            except KeyboardInterrupt:
                print("\nInterrupted by user")
                self.running = False
                break
            except Exception as e:
                if self.running:
                    print(f" Error sending: {e}")
                break


class ServerDevice(Device):
    """Device yang jadi Server (menunggu koneksi)"""
    def __init__(self, port=DEFAULT_PORT):
        super().__init__("Server Device")
        self.port = port
        self.host = '0.0.0.0'  # Listen on all interfaces
    
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)
        except Exception as e:
            print(f" Failed to start server: {e}")
            return
        
        local_ip = get_local_ip()
        
        print("\n" + "=" * 70)
        print("  DEVICE 1 - SERVER MODE")
        print("=" * 70)
        print(f" Shared Key: {self.key}")
        print(f" Server IP: {local_ip}")
        print(f" Port: {self.port}")
        print("\n  PENTING: Beritahu IP ini ke Device 2!")
        print(f"   Device 2 harus connect ke: {local_ip}")
        print("\nWaiting for Device 2 to connect...")
        print("=" * 70)
        
        try:
            client_socket, address = server_socket.accept()
            print(f"\n Device 2 connected from {address[0]}:{address[1]}")
            print("=" * 70)
            print(" Chat started! Type your message and press Enter.")
            print(" Type 'quit' to exit.")
            print("=" * 70)
            print()
            
            # Thread untuk menerima pesan
            receive_thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
            receive_thread.daemon = True
            receive_thread.start()
            
            # Main thread untuk mengirim pesan
            self.send_messages(client_socket)
            
            client_socket.close()
        except KeyboardInterrupt:
            print("\n Server stopped by user")
        finally:
            server_socket.close()


class ClientDevice(Device):
    """Device yang jadi Client (connect ke server)"""
    def __init__(self, server_ip, port=DEFAULT_PORT):
        super().__init__("Client Device")
        self.server_ip = server_ip
        self.port = port
    
    def start(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print("\n" + "=" * 70)
        print(" DEVICE 2 - CLIENT MODE")
        print("=" * 70)
        print(f" Shared Key: {self.key}")
        print(f" Connecting to Server: {self.server_ip}:{self.port}")
        print("=" * 70)
        
        try:
            client_socket.connect((self.server_ip, self.port))
            print("\n Connected to Device 1!")
            print("=" * 70)
            print(" Chat started! Type your message and press Enter.")
            print(" Type 'quit' to exit.")
            print("=" * 70)
            print()
            
            # Thread untuk menerima pesan
            receive_thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
            receive_thread.daemon = True
            receive_thread.start()
            
            # Main thread untuk mengirim pesan
            self.send_messages(client_socket)
            
        except Exception as e:
            print(f"\n Connection failed: {e}")
            print("\n Tips:")
            print("   1. Pastikan Device 1 sudah jalan (server mode)")
            print("   2. Pastikan IP address benar")
            print("   3. Pastikan kedua device dalam network yang sama")
            print("   4. Cek firewall (mungkin block port 5555)")
        finally:
            client_socket.close()


# ==================== MAIN PROGRAM ====================

def print_instructions():
    print("\n" + "=" * 70)
    print("📚 CARA SETUP 2 DEVICE BERBEDA:")
    print("=" * 70)
    print("""
1. DEVICE 1 (Server):
   - Jalankan program ini, pilih mode 1 (Server)
   - Catat IP address yang muncul
   - Tunggu Device 2 connect

2. DEVICE 2 (Client):
   - Jalankan program ini di device lain
   - Pilih mode 2 (Client)
   - Masukkan IP address dari Device 1
   - Mulai chat!

CATATAN PENTING:
 Kedua device harus dalam network yang sama (WiFi/LAN sama)
 Firewall mungkin perlu setting untuk allow port 5555
 Gunakan IP local (192.168.x.x), bukan 127.0.0.1
    """)
    print("=" * 70)

def main():
    print("\n" + "=" * 70)
    print(" DES ENCRYPTED CHAT SYSTEM - 2 DIFFERENT DEVICES")
    print("=" * 70)
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        print("\nPilih mode:")
        print("1. Device 1 (Server) - Tunggu koneksi")
        print("2. Device 2 (Client) - Connect ke server")
        print("3. Lihat instruksi setup")
        print("=" * 70)
        mode = input("\nMasukkan pilihan (1/2/3): ").strip()
    
    if mode == '1':
        server = ServerDevice(port=DEFAULT_PORT)
        server.start()
    elif mode == '2':
        if len(sys.argv) > 2:
            server_ip = sys.argv[2]
        else:
            server_ip = input("\n Masukkan IP address Device 1 (Server): ").strip()
        
        if not server_ip:
            print(" IP address tidak boleh kosong!")
            return
        
        client = ClientDevice(server_ip, port=DEFAULT_PORT)
        client.start()
    elif mode == '3':
        print_instructions()
    else:
        print(" Pilihan tidak valid!")


if __name__ == "__main__":
    main()