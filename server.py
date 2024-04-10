import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # localhost
PORT = 55555
ADDR = (HOST, PORT)

# List to store client connections
clients = []

# Function to handle client connections
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    # Send a welcome message to the client
    conn.send("Welcome to the chat room!".encode())

    # Loop to handle incoming messages
    while True:
        try:
            message = conn.recv(1024).decode()
            if message:
                print(f"[{addr}] {message}")
                broadcast(message, conn)
            else:
                remove(conn)
        except:
            continue

# Function to broadcast messages to all clients
def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message.encode())
            except:
                remove(client)

# Function to remove client from the chat
def remove(conn):
    if conn in clients:
        clients.remove(conn)

# Main function to start the server
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()

    print("[SERVER] Server is listening...")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
