import socket  # Import the socket module to enable network communication
import threading  # Import the threading module to manage threads for receiving messages

host = socket.gethostname()  # Define the server's IP address to connect to
port = 1233  # Define the port number to connect to on the server

# Function to receive messages from the server in a separate thread
def receive_messages(ClientSocket):
    while True:  # Infinite loop to continuously receive messages
        try:
            message = ClientSocket.recv(2048).decode('utf-8')  # Receive a message from the server and decode it
            if not message:  # If no message is received, break the loop
                break
            print(message)  # Print the received message to the console
        except:
            print("Disconnected from server.")  # If there is an error, print a disconnection message
            break  # Exit the loop if an error occurs

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a new socket
print('Connecting to server...')  # Print a message indicating that the client is trying to connect to the server
try:
    ClientSocket.connect((host, port))  # Attempt to connect to the server at the specified host and port

    # Start a new thread to handle receiving messages from the server
    threading.Thread(target=receive_messages, args=(ClientSocket,)).start()

    while True:  # Infinite loop to continuously allow the user to send messages
        message = input()  # Prompt the user to input a message
        ClientSocket.send(str.encode(message))  # Send the message to the server
        if message.upper() == "BYE":  # If the user types "BYE", break the loop and disconnect
            break
except Exception as e:  # If an error occurs during connection or communication, handle it
    print(f"Connection error: {e}")  # Print the error message
finally:
    ClientSocket.close()  # Close the socket connection after the loop ends
