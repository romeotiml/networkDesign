Readme File

Programming Project Phase 4: Enhance RDT 2.2 to RDT 3.0 over an unreliable UDP channel with simulations of ACK packer bit-error, Data packet bit-error, ACK packer loss, Data packet loss and be able to recover the errors.

Was done as a group

Group members:
Brendan Pham
Romeo Tim-Louangphixai
Chad Abboud

OS used:
Windows 10 & 11

Language:
Python 3.12.1

Files submitted:
client.py
server.py


Instructions: This phase was run using PyCharm with the latest Python update.

The code was created to simplify the use and make it cleaner. To run the program, you need to be able to use an IDE or any application that allows you to use Python. 

Next, change the necessary 'file_path' in client.py and 'output_directory' in server.py After that is complete, start by running the server script and then the client script; Depending on your .jpeg file size, you should get an output located in your designated 'output_directory'.

UDP Client: Only need to change the 'file_path' in the client script to know what directory the .jpeg is being taken from; Please change the Scenario Options to whatever rate the user would prefer. (ex. 0.05 = 5% Error)

UDP Server: The only change needed here is the 'output_directory'; this is for where your .jpeg output will be placed after running the scripts. Please change the Scenario Options to whatever rate the user would prefer. (ex. 0.05 = 5% Error)

Note: Ensure that both the client and server files are running and have access to each other over the network. Make sure to provide correct file paths and directory paths as input when prompted. 
Depending on your network configuration, you may need to adjust firewall settings to allow communication between the client and server. The server and client use port 12001 for communication. 
Ensure this port is open on both machines and not blocked by a firewall. The scripts simulate an unreliable channel with a certain probability of bit errors in the transmitted data. 
This behavior is intentional to demonstrate the handling of errors in data transmission. Both the client and server print logs to the terminal, indicating the progress of file transmission and the occurrence of any errors or retries due to packet loss or corruption.
