import socket
from Models.end_user import EndUser
import variables


def _get_client_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", variables.INITIALIZATION_PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            user_params = conn.recv(1024).decode().split(",")
            print(f"{user_params[0]} wants to connect. do you approve? Y/N")
            answer = input()
            conn.send(answer.lower().encode())
            if answer.lower() == "y":
                return EndUser(user_params[0], addr[0], user_params[1], user_params[2], False)
            else:
                return False


def initialize_connection_server():
    user = None
    while not user:
        user = _get_client_connection()
    return user


def initialize_connection_client(server_user: EndUser):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((variables.SERVER_IP, variables.INITIALIZATION_PORT))
        s.send(f"{server_user.name},{server_user.chat_port},{server_user.voice_port}".encode())
        res = s.recv(1024).decode()
        if res == "y":
            return True
        else:
            return False
