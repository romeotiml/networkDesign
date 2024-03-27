from socket import *
import hashlib
import os

SERVER_PORT = 12001

def calculate_checksum(data):
    return hashlib.md5(data).digest()

def start_udp_server():
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', SERVER_PORT))
    print(f"Server listening on port {SERVER_PORT}.")

    output_directory = r'C:\Users\romeo\Desktop'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file_path = os.path.join(output_directory, 'output.jpg')

    try:
        with open(output_file_path, 'wb') as file:
            seq_num = 0
            while True:
                packet, client_address = server_socket.recvfrom(2048)
                print(f"Packet received from {client_address}.")
                # Simulate ACK
                server_socket.sendto(b'ACK', client_address)
                file.write(packet)  # Simplified; real implementation would check packet integrity
                print(f"Data written to file. ACK sent to {client_address}.")
    finally:
        server_socket.close()
        print("Server shutdown.")

if __name__ == "__main__":
    start_udp_server()
