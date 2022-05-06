import socket
import threading
import sys
import time
# TODO: Implement a client that connects to your server to chat with other clients here
# Use sys.stdout.flush() after print statements

inputs = sys.argv
hostname = inputs[3]
port = int(inputs[5])
username = inputs[7]
passcode = inputs[9]
username_and_passcode = username + " " + passcode

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((hostname, port))

client.send(username_and_passcode.encode())
passcode_confirmation = client.recv(1024).decode()


def client_start_output():
    if passcode_confirmation == "decline":
        print("Incorrect passcode")
        sys.stdout.flush()
        client.close()
        exit()
    else:
        print(f"Connected to {hostname} on port {port}")
        sys.stdout.flush()

        receive_message_thread = threading.Thread(target=receive_message_from_server)
        send_message_thread = threading.Thread(target=send_message_to_server)
        receive_message_thread.start()
        send_message_thread.start()


def receive_message_from_server():
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
            sys.stdout.flush()
        except:
            client.close()
            break


def send_message_to_server():
    while True:
        try:
            message_original = f"{username}: {input()}"
            message_modified = check_for_shortcuts(message_original)
            client.send(message_modified.encode())

            if ":Exit" in message_original:
                client.close()
                break
        except:
            client.close()
            break


def check_for_shortcuts(message_original):
    message_modified = message_original.replace(":)", "[feeling happy]").replace(":(", "[feeling sad]").replace(":mytime", get_time(is_plus_one_hour=False)).replace(":+1hr", get_time(is_plus_one_hour=True))
    return message_modified


def get_time(is_plus_one_hour):
    display_time = time.localtime()
    if is_plus_one_hour:
        secs = time.time() + 3600
        display_time = time.localtime(secs)

    new_time = time.asctime(display_time)
    return new_time


if __name__ == "__main__":
    client_start_output()
