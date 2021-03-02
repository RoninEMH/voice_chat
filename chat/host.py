import socket
import threading
from connection import Connection


class Host(Connection):
    def __init__(self, name, port):
        super().__init__(name)
        # try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(('localhost', port))
            server.listen(1)
            print('Waiting for a connection...')
            with server.accept()[0] as connection:
                print('connection accepted')
                threading.Thread(target=self.read, args=(connection,)).start()
                self.write(connection)
        # except Exception as e:
        # print(e)
        # print('hello')
        # print('placeholder - error occurred with server')

    def close(self):
        super().close()
