# 🗨️ Socket Chat Application

📌 Description

This project is an implementation of a Client–Server Chat Application built with Python sockets.
The system allows multiple clients to connect to a central server, send public or private messages, and communicate in real-time.

## ⚙️ Technologies Used

Python 3

socket – for TCP/IP communication

threading / _thread – to handle multiple clients concurrently

sys – for server shutdown and process handling

I/O – for user input and message display

## ✨ Features

Supports multiple clients simultaneously via threads

Broadcast messages to all connected users

Private messaging using @username

Graceful disconnection with the BYE command

Server activity logs saved to server_logs.txt

Admin command terminate to shut down the server safely

## 📂 File Structure

 server.py

 client.py 
 
 server_logs.txt
 

 
## 🚀 How to Run
Requirements:

Python 3 installed

No external dependencies required (only Python standard library)

Run the Server
python server.py

Run a Client
python client.py

Usage Instructions:

Start the server first.

Then run one or more clients.

Each client will be asked to enter a unique username.

To send a public message, just type and press Enter.

To send a private message, use:

@username your message


To disconnect: type BYE.

To shut down the server: in the server terminal, type terminate.

## 👨‍💻 Author

Shahar Rushetzky

📞 Phone: +972 52-7729726

📧 Email: sroshetzky@gmail.com

🔗 LinkedIn: [Shahar Rushetzky](https://www.linkedin.com/in/shahar-rushetzky/)
