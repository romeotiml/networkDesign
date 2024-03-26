# Romeo Tim-Louangphixai, Chad Abboud, Brendan Pham
# Student ID: 01819835
# Network Design: Principles, Protocols & Applications
# Programming Project Phase 3: Implement RDT 2.2 over an unreliable UDP channel with bit-errors

# This file is for the creation and management of the UDP Client

from socket import socket, AF_INET, SOCK_DGRAM, timeout
import hashlib
import struct

# Constants
SERVER_ADDR = ('localhost', 12000)
CLIENT_TIMEOUT = 2.0  # Timeout for ACK waiting
PACKET_SIZE = 1024  # Data payload size in bytes

def make_packet(seq_num, data=b''):
    """Creates a packet with a sequence number and data, using MD5 for checksum."""
    seq_bytes = struct.pack('I', seq_num)  # Convert sequence number to bytes
    checksum = calculate_checksum(seq_bytes + data)
    return checksum + seq_bytes + data

def calculate_checksum(data):
    """Calculates checksum using MD5 hashing."""
    md5 = hashlib.md5()
    md5.update(data)
    return md5.digest()

def verify_checksum(packet):
    """Verifies if the packet's checksum matches its contents, using MD5."""
    received_checksum = packet[:16]  # MD5 checksum size
    seq_and_data = packet[16:]
    expected_checksum = calculate_checksum(seq_and_data)
    return received_checksum == expected_checksum

def send_file(file_path):
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.settimeout(CLIENT_TIMEOUT)
        
        # Open the file
        with open(file_path, 'rb') as f:
            seq_num = 0
            while True:
                data = f.read(PACKET_SIZE)
                if not data:
                    break  # File has been read completely
                
                while True:
                    packet = make_packet(seq_num, data)
                    s.sendto(packet, SERVER_ADDR)
                    try:
                        # Wait for ACK
                        ack_packet, _ = s.recvfrom(1024)
                        if verify_checksum(ack_packet) and ack_packet[16:] == struct.pack('I', seq_num):
                            print(f"ACK received for seq {seq_num}")
                            seq_num = (seq_num + 1) % 2  # Toggle sequence number
                            break  # Move to next packet
                    except timeout:
                        print("Timeout, resending packet")
    finally:
        s.close()

if __name__ == "__main__":
    file_path = input('Enter the path of the JPEG file you wish to send: ')
    send_file(file_path)

