from abc import ABC, abstractmethod
import parsing


class Connection(ABC):
    @abstractmethod
    def __init__(self, name, queue):
        self.name = name
        self.closed = False
        self.queue = queue

    def read(self, socket):
        while not self.closed:
            try:
                data = socket.recv(1024)
                if data:
                    print(data.decode())
                else:
                    print('The other user has disconnected')
                    self.close()
                    break
            except ConnectionAbortedError:
                print('You ended the conversation')
                self.close()
                break
            except ConnectionResetError:
                print('The other user has disconnected')
                self.close()
                break

    def write(self, socket):
        p = parsing.Parser(self.queue)
        while not self.closed:
            user_input = p.parse(input(), self)
            if not self.closed:
                if user_input:
                    try:
                        socket.send(bytes(self.name + ": " + user_input, 'utf-8'))
                    except:
                        print('err')
                        self.close()
                        break

    @abstractmethod
    def close(self):
        self.closed = True
