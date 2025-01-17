import socket  # Import the socket module to enable communication over the network
from _thread import *  # Import threading functions to handle clients concurrently
import sys  # Import sys to exit the server

host = socket.gethostname()  # Set the IP address of the server
port = 1233  # Set the port number the server will listen on
clients = {}  # Initialize an empty dictionary to store client names and their connections
server_running = True  # Variable to control the server's running status
ServerSocket = None  # Declare the ServerSocket globally
logs = []  # List to store all logs

# Function to start the server and listen for incoming connections
def start_server(host, port):
    global server_running, ServerSocket  # Declare we're using global variables
    ServerSocket = socket.socket()  # Create a new socket object for the server
    try:
        ServerSocket.bind((host, port))  # Bind the socket to the host IP and port
    except socket.error as e:  # If an error occurs during binding
        print(str(e))  # Print the error message
        logs.append(f"Error during binding: {e}")  # Add the error to logs
        sys.exit()  # Exit the server if binding fails
    print(f"Server is listening on the port {port}...\n" 
    f"Type 'terminate' to shut down the server.")  # Print a message indicating the server is now listening
    logs.append(f"Server started and listening on port {port}")  # Log server start
    ServerSocket.listen()  # Start listening for incoming client connections
    accept_connections()  # Call the function to accept incoming connections

# Function to accept incoming client connections
def accept_connections():
    global server_running
    while server_running:  # Infinite loop to continuously accept incoming client connections
        try:
            Client, address = ServerSocket.accept()  # Accept a new client connection
            print(f"Connected to: {address[0]}:{address[1]}")  # Print the client's IP address and port
            logs.append(f"Connected to: {address[0]}:{address[1]}")  # Log the connection
            start_new_thread(client_handler, (Client,))  # Create a new thread to handle the client
        except socket.error:  # Handle the error if server is stopped
            break  # Break out of the loop if the server is stopped

# Function to handle communication with each client
def client_handler(connection):
    connection.send(str.encode("Enter your unique name: "))  # Ask the client for a unique name
    name = connection.recv(2048).decode('utf-8')  # Receive the client's name
    clients[name] = connection  # Store the client's connection in the clients dictionary with their name as the key
    logs.append(f"Client '{name}' connected.")  # Log the client's connection
    connection.send(str.encode(f"Welcome {name}! Type 'BYE' to disconnect,\n"
                               f"Type '@<client_name> to send a private message.\n"
                               f"to send message to all, just send the message freely!"))  # Send a welcome message to the client with instructions

    while True:  # Infinite loop to continuously receive messages from the client
        try:
            data = connection.recv(2048)  # Receive a message from the client
            if not data:  # If no data is received, the client has disconnected
                break
            message = data.decode('utf-8')  # Decode the received message to string

            if message.upper() == "BYE":  # Check if the client wants to disconnect
                break  # Exit the loop if the message is "BYE"

            # If the message starts with "@", it's a private message
            elif message.startswith("@"):
                parts = message.split(" ", 1)  # Split the message into target client and message parts
                if len(parts) > 1:  # If the message contains a target and content
                    target_name = parts[0][1:]  # Extract the target client's name (without the "@")
                    target_message = parts[1]  # Extract the actual message to send

                    if target_name in clients:  # Check if the target client exists
                        target_connection = clients[target_name]  # Get the target client's connection
                        target_connection.sendall(str.encode(f"{name}: {target_message}"))  # Send the private message
                        logs.append(f"Private message from {name} to {target_name}: {target_message}")  # Log the private message
                    else:
                        connection.sendall(str.encode(
                            f"Client {target_name} not found.\n"))  # Inform the sender if the client is not found
                else:
                    connection.sendall(
                        str.encode("Invalid command.\n"))  # Handle cases where the message format is invalid

            # If the message doesn't start with "@", it is a general message to all clients
            else:
                broadcast_message(name, message)  # Broadcast the message to all clients
                logs.append(f"Message from {name}: {message}")  # Log the general message

        except Exception as e:  # Catch any exceptions (client disconnecting unexpectedly)
            print(f"Error with client {name}: {e}. Disconnecting.")  # Print the error and disconnect the client
            logs.append(f"Error with client {name}: {e}. Disconnecting.")  # Log the error
            break  # Exit the loop if an exception occurs

    # Synchronously remove the client from the list and close the connection
    print(f"{name} disconnected.")  # Print the client's name when they disconnect
    logs.append(f"Client '{name}' disconnected.")  # Log the disconnection
    del clients[name]  # Remove the client from the clients dictionary
    connection.close()  # Close the client's connection

# Function to broadcast a message to all clients except the sender
def broadcast_message(sender_name, message):
    for name, connection in list(clients.items()):  # Use a list copy to prevent runtime errors
        if name != sender_name:  # Skip sending the message to the sender
            try:
                connection.sendall(str.encode(f"{sender_name}: {message}"))  # Send the message to the client
            except:
                connection.close()  # If there is an error sending, close the connection
                del clients[name]  # Remove the client from the list of active clients

# Function to handle server shutdown from terminal
def shutdown_server():
    global server_running  # Access the global server_running variable
    server_running = False  # Set the server status to False, which will stop the server
    print("Server is shutting down...")  # Print the shutdown message
    logs.append("Server is shutting down...")  # Log the shutdown event
    try:
        for connection in list(clients.values()):  # Use a list copy to prevent runtime errors
            try:
                connection.sendall(str.encode("SERVER_SHUTDOWN"))  # Notify all clients that the server is shutting down
                connection.close()  # Close each client connection
            except:
                pass
    finally:
        save_logs_to_file()  # Save logs to a file
        if ServerSocket:
            ServerSocket.close()  # Close the server socket
        print("Server has been terminated.")
        sys.exit()  # Exit the program

# Function to save logs to a text file
def save_logs_to_file():
    with open("server_logs.txt", "w", encoding="utf-8") as file:
        for log in logs:
            file.write(log + "\n")
    print("Logs saved to 'server_logs.txt'.")

# Start a thread to listen for shutdown commands from the terminal
def listen_for_shutdown():
    while True:  # Infinite loop to continuously listen for shutdown commands
        command = input()  # Get input from the terminal
        if command.lower() == "terminate":  # If the input is "terminate", shut down the server
            shutdown_server()  # Call the function to shut down the server

# Start the server and accept connections
start_new_thread(listen_for_shutdown, ())  # Start the shutdown listener in a separate thread
start_server(host, port)  # Start the server to accept client connections
