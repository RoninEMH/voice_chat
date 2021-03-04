import client
import host
import queue
answer = int(input('are you the host?'))
if answer:
    x = host.Host('alice', 12345, queue.SimpleQueue())
else:
    x = client.Client('bob', 'localhost', 12345,queue.SimpleQueue())
