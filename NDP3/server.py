# Romeo Tim-Louangphixai, Chad Abboud, Brendan Pham
# Network Design: Principles, Protocols & Applications
# Programming Project Phase 3: Implement RDT 2.2 over an unreliable UDP channel with bit-errors

# This file is for the creation and management of the UDP server

from socket import *
import hashlib
import os

SERVER_PORT = 12001


def calculate_checksum(data):
    """Calculate the MD5 checksum for data."""
    return hashlib.md5(data).digest()


def start_udp_server(port=SERVER_PORT):
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', port))
    print(f"Server listening on port {port}.")

    output_directory = r'C:\Users\romeo\Desktop'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file_path = os.path.join(output_directory, 'output.jpg')

    try:
        with open(output_file_path, 'wb') as file:
            print("Ready to receive data...")
            while True:
                packet, client_address = server_socket.recvfrom(2048)
                seq_num_bytes = packet[:4]
                received_checksum = packet[4:20]
                data = packet[20:]

                calculated_checksum = calculate_checksum(seq_num_bytes + data)
                if calculated_checksum == received_checksum:
                    file.write(data)
                    print(f"Valid packet received from {client_address}.")
                    server_socket.sendto(b'ACK', client_address)
                else:
                    print(f"Checksum mismatch from {client_address}. Discarded.")
    finally:
        server_socket.close()
        print("Server shutdown.")


if __name__ == "__main__":
    start_udp_server()
