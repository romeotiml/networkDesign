# Importing necessary libraries
from socket import *
import os
import hashlib

# Constants
SEQUENCE_SIZE = 32  # Size of the sequence number in bits
PACKET_SIZE = 1024  # Packet size in bytes


# Function to calculate checksum using MD5 hashing
def calculate_checksum(data):
    hash_object = hashlib.md5()
    hash_object.update(data)
    checksum = hash_object.digest()
    return checksum


# Function to validate packet checksum
def validate_checksum(seq_num, checksum, data):
    expected_checksum = calculate_checksum(seq_num.to_bytes(SEQUENCE_SIZE // 8, 'big') + data)
    return checksum == expected_checksum


# Function to start the UDP server and receive RDT 2.2 packets
def start_udp_server(server_port, directory_path):
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', server_port))
    print("The UDP server is now ready to receive!\n")

    # Ensure directory_path is correctly handled
    if not os.path.isdir(directory_path):
        print(f"The provided directory path does not exist: {directory_path}")
        return

    output_file_path = os.path.join(directory_path, 'output.jpg')

    with open(output_file_path, "wb") as file:
        expected_seq_num = 0
        while True:
            packet, client_address = server_socket.recvfrom(1024 + SEQUENCE_SIZE // 8 + hashlib.md5().digest_size)
            seq_num_bytes = packet[:SEQUENCE_SIZE // 8]
            checksum = packet[SEQUENCE_SIZE // 8:SEQUENCE_SIZE // 8 + hashlib.md5().digest_size]
            data = packet[SEQUENCE_SIZE // 8 + hashlib.md5().digest_size:]

            # Check for end of file marker
            if data == b"EOF":
                break

            seq_num = int.from_bytes(seq_num_bytes, 'big')

            # Validate packet using checksum
            if validate_checksum(seq_num, checksum, data) and seq_num == expected_seq_num:
                file.write(data)
                expected_seq_num = (expected_seq_num + 1) % (2 ** SEQUENCE_SIZE)
                ack_packet = seq_num_bytes + checksum + b"ACK"
                server_socket.sendto(ack_packet, client_address)
            else:
                nak_packet = seq_num_bytes + checksum + b"NAK"
                server_socket.sendto(nak_packet, client_address)

    server_socket.close()
    print("File received and written successfully.")


if __name__ == "__main__":
    port = 12000
    directory_path = input('Enter the directory path to store the received JPEG file: ')
    start_udp_server(port, directory_path)
