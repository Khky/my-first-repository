import socket

# Raspberry Pi IP address and port
rpi_ip = "192.168.1.100"  # Replace with your Raspberry Pi's IP address
rpi_port = 5005  # Replace with the desired port number

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the Raspberry Pi's IP address and port
sock.bind((rpi_ip, rpi_port))

while True:
    # Receive data from the Arduino
    data, addr = sock.recvfrom(1024)
    print("Received data from Arduino:", data.decode())

    # Send a response back to the Arduino
    response = "Message received!"
    sock.sendto(response.encode(), addr)
