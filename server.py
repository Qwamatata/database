import socket
import IlyasMessageProtocol
import threading
import main
import json

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 10052))
server_socket.listen()


def client_handler(client_socket_: socket.socket):
    query = IlyasMessageProtocol.receive(client_socket_)[1]
    if query != '':
        response = main.handle_query(query)
        if isinstance(response, str):
            IlyasMessageProtocol.send(client_socket_, response.encode(), 'TXT', 'a')
        else:
            IlyasMessageProtocol.send(client_socket_, json.dumps(response[0]).encode(), 'JSN', 'a')


while True:
    client = server_socket.accept()
    client_socket = client[0]
    thread = threading.Thread(target=client_handler, args=[client_socket])
    thread.start()
