from socket import *
import hashlib
import os

SERVER_PORT = 12001
TIMEOUT = 5  # seconds
RETRY_LIMIT = 20
WINDOW_SIZE = 4  # Number of packets in the receive window


def calculate_checksum(data):
    return hashlib.md5(data).digest()


def start_udp_server(port=SERVER_PORT):
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', port))
    print(f"Server listening on port {port}.")

    output_directory = r"C:\Users\Brendan's PP\Desktop"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file_path = os.path.join(output_directory, 'output.jpg')

    try:
        with open(output_file_path, 'wb') as file:
            print("Ready to receive data...")
            expected_seq_num = 0
            receive_window = [None] * WINDOW_SIZE  # Initialize receive window

            while True:
                packet, client_address = server_socket.recvfrom(2048)
                seq_num_bytes = packet[:4]
                received_checksum = packet[4:20]
                data = packet[20:]

                calculated_checksum = calculate_checksum(seq_num_bytes + data)
                seq_num = int.from_bytes(seq_num_bytes, byteorder='big')

                if calculated_checksum == received_checksum and seq_num >= expected_seq_num:
                    # Check if packet falls within the receive window
                    window_index = seq_num % WINDOW_SIZE
                    if receive_window[window_index] is None:
                        receive_window[window_index] = data
                        print(f"Valid packet {seq_num} received from {client_address}.")
                    else:
                        print(f"Duplicate packet {seq_num} received from {client_address}.")

                    # Send cumulative ACK for the last received packet
                    server_socket.sendto(seq_num_bytes, client_address)

                    # Slide receive window if contiguous packets are received
                    while receive_window[0] is not None:
                        file.write(receive_window[0])
                        receive_window.pop(0)
                        receive_window.append(None)
                        expected_seq_num += 1
                        print(f"Packet {expected_seq_num - 1} written to file.")

                else:
                    print(f"Invalid packet or out-of-order packet {seq_num} received from {client_address}. Discarded.")

    finally:
        server_socket.close()
        print("Server shutdown.")


if __name__ == "__main__":
    start_udp_server()
