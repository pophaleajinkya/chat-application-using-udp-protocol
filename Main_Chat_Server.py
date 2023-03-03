import socket
import sys
import select

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific IP address and port
server_address = ('localhost', 20000)
sock.bind(server_address)
# List of active clients (IP, port)
clients = []

print('Server Initialized and is running.......')

while True:
    # Wait for incoming message
    try:
        # Wait for data to be received
        ready = select.select([sock], [], [], 1)
        if ready[0]:
            data, address = sock.recvfrom(4096)
            # Check message type
            msg_type = data[:3].decode()
            msg_body = data[3:].decode()

            if msg_type == 'GRE':
                # Register client if not already registered
                if address not in clients:
                    clients.append(address)
                    print('Client', address, 'has joined the chat')

            elif msg_type[:3] == 'MES':
                # Broadcast message to all active clients
                for client in clients:
                    # if client != address: (Excluding the Sender)
                    # In current scenario, the message sent is received by the sender too...
                    sock.sendto(('From' + str(address) + ': ' + msg_body).encode(), client)
    except KeyboardInterrupt:
        # press Ctrl+C to shut down the server.
        print('Server shutting down')
        sock.close()
        sys.exit()
