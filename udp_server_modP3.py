from socket import socket, AF_INET, SOCK_DGRAM
import hashlib
import struct

SERVER_ADDR = ('localhost', 12000)

def receive_file():
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(SERVER_ADDR)
    
    expected_seq_num = 0
    try:
        while True:
            packet, addr = s.recvfrom(4096)
            if not packet:
                break  # No more data, stop the server
                
            if verify_checksum(packet) and packet[16:20] == struct.pack('I', expected_seq_num):
                print(f"Packet {expected_seq_num} received correctly")
                # Extract data and write or process it as needed
                
                # Send ACK
                ack_packet = make_packet(expected_seq_num)
                s.sendto(ack_packet, addr)
                expected_seq_num = (expected_seq_num + 1) % 2  # Toggle expected sequence number
            else:
                # If packet is corrupted or unexpected sequence number, send ACK for the last correct packet
                ack_packet = make_packet((expected_seq_num - 1) % 2)
                s.sendto(ack_packet, addr)
    finally:
        s.close()

def make_packet(seq_num, data=b''):
    """Reuses the make_packet function from client for ACK packet creation."""
    return calculate_checksum(struct.pack('I', seq_num) + data) + struct.pack('I', seq_num) + data

def calculate_checksum(data):
    """Checksum calculation using MD5, identical to the client's function."""
    md5 = hashlib.md5()
    md5.update(data)
    return md5.digest()

def verify_checksum(packet):
    """Checksum verification, similar to the client's logic."""
    received_checksum = packet[:16]
    seq_and_data = packet[16:]
    expected_checksum = calculate_checksum(seq_and_data)
    return received_checksum == expected_checksum

if __name__ == "__main__":
    receive_file()
    
