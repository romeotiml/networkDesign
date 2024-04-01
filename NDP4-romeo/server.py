# Romeo Tim-Louangphixai, Chad Abboud, Brendan Pham
# Network Design: Principles, Protocols & Applications
# Programming Project Phase 4: Implement RDT 3.0 over an unreliable UDP channel with bit-errors and loss

# This file is for the creation and management of the UDP server

from socket import *
import hashlib
import os

SERVER_PORT = 12001
SEQUENCE_SIZE = 4

def calculate_checksum(data):
    """Calculate the MD5 checksum for data."""
    return hashlib.md5(data).digest()

def start_udp_server(port=SERVER_PORT):
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', port))
    print(f"Server listening on port {port}.")

    output_directory = 'C:\\Users\\romeo\\Desktop'  # Ensure this path is correct
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file_path = os.path.join(output_directory, 'output.jpg')

    expected_seq_num = 0

    try:
        with open(output_file_path, 'wb') as file:
            print("Ready to receive data...")
            while True:
                packet, client_address = server_socket.recvfrom(2048)
                seq_num_bytes = packet[:4]
                received_checksum = packet[4:20]
                data = packet[20:]
                seq_num = int.from_bytes(seq_num_bytes, byteorder='big')

                calculated_checksum = calculate_checksum(seq_num_bytes + data)
                if calculated_checksum != received_checksum:
                    print(f"Checksum mismatch for packet {seq_num}. Packet discarded.")
                    continue

                if seq_num == expected_seq_num:
                    print(f"Packet {seq_num} received and written.")
                    file.write(data)
                    server_socket.sendto(seq_num_bytes, client_address)  # Send ACK for received packet
                    expected_seq_num += 1
                else:
                    print(f"Out-of-order packet {seq_num} received. Ignoring and waiting for packet {expected_seq_num}.")
                    # Do not send ACK for out-of-order packets; wait for the correct packet

    finally:
        server_socket.close()
        print("Server shutdown.")

if __name__ == "__main__":
    start_udp_server()
