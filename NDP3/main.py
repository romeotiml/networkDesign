# Romeo Tim-Louangphixai, Chad Abboud, Brendan Pham
# Network Design: Principles, Protocols & Applications
# Programming Project Phase 3: Implement RDT 2.2 over an unreliable UDP channel with bit-errors

# Run this script twice from two separate terminals for the server and client respectively.
# Use the argument 'server' to run the server, and any other argument to run the client.

import sys
import client
import server

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        print("Starting server...")
        server.start_udp_server()
    else:
        print("Starting client after a short delay...")
        client.send_rdt_packets()
