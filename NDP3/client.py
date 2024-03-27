from socket import *
import hashlib
from bit_error_simulation import introduce_bit_error
import time

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12001
TIMEOUT = 2  # seconds
RETRY_LIMIT = 5  # Max retries before giving up

def send_rdt_packets():
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)

    file_path = r'C:\Users\romeo\Desktop\corgi.jpeg'
    error_rate = 0.02
    seq_num = 0
    retries = 0

    with open(file_path, "rb") as file:
        while True:
            data = file.read(1024)
            if not data:
                break  # End of file
            rdt_packet = introduce_bit_error(data, error_rate)
            client_socket.sendto(rdt_packet, (SERVER_ADDRESS, SERVER_PORT))
            print(f"Packet {seq_num} sent, waiting for ACK...")

            while True:
                try:
                    ack_packet, _ = client_socket.recvfrom(1024)
                    print("ACK received.")
                    retries = 0  # Reset retries after successful ACK
                    break  # Move to the next packet
                except timeout:
                    retries += 1
                    print(f"Timeout, resending packet {seq_num}... (Retry {retries})")
                    if retries >= RETRY_LIMIT:
                        print("Max retries reached. Giving up.")
                        return
                    client_socket.sendto(rdt_packet, (SERVER_ADDRESS, SERVER_PORT))
            seq_num += 1

    client_socket.close()
    print("File transfer completed.")
