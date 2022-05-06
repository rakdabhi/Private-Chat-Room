import socket
import threading
import sys

# TODO: Implement all code for your server here
# Use sys.stdout.flush() after print statements

inputs = sys.argv
hostname = "127.0.0.1"
port = int(inputs[3])
passcode = inputs[5]
clients_dict = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((hostname, port))
server.listen()


def server_start_output():
    print(f"Server started on port {port}. Accepting connections")
    sys.stdout.flush()


def send_message_to_all_clients(client, message):
    print(message)
    sys.stdout.flush()
    for c in clients_dict:
        if c != client:
            c.send(message.encode())


def client_thread(client):
    while True:
        try:
            message = client.recv(1024).decode()
            if ":Exit" in message:
                remove_client(client=client)
                break
            send_message_to_all_clients(client=client, message=message)
        except:
            remove_client(client=client)
            break


def add_client(client, username):
    clients_dict[client] = username
    send_message_to_all_clients(client=client, message=f"{username} joined the chatroom")


def remove_client(client):
    username = clients_dict[client]
    del clients_dict[client]
    client.close()
    send_message_to_all_clients(client=client, message=f"{username} left the chatroom")


def receive_messages_from_clients():
    while True:
        client, address = server.accept()

        client_input = client.recv(1024).decode().split()
        client_username, client_passcode = client_input[0], client_input[1]
        if client_passcode != passcode:
            client.send("decline".encode())
            client.close()
        else:
            client.send("accept".encode())
            add_client(client=client, username=client_username)

            thread = threading.Thread(target=client_thread, args=(client,))
            thread.start()


if __name__ == "__main__":
    server_start_output()
    receive_messages_from_clients()
