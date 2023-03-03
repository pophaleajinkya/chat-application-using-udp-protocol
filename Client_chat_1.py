import socket
import sys
import select

# Create a UDP socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.connect(('localhost', 20000))

# Send a greeting to the server
client.send(bytes('GREETINGS', 'utf-8'))
print('Welcome to the chat room!')
print('Type your message and press Enter to send it')

while True:
    # Wait for incoming message or input from standard input
    try:
        # Wait for data to be received
        ready = select.select([client, sys.stdin], [], [], 1)
        if ready[0]:
            for r in ready[0]:
                if r == client:
                    # Receive incoming message from the server
                    data, address = client.recvfrom(4096)

                    # Print incoming message
                    print(data.decode())

                elif r == sys.stdin:
                    # Read message from standard input and send to the server
                    message = sys.stdin.readline().strip()
                    client.send(bytes('MES' + message, 'utf-8'))

    except KeyboardInterrupt:
        # Handle Ctrl-C
        print(' Leaving chat room')
        client.close()
        sys.exit()
