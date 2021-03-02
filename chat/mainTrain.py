import client
import host
from parsing import parser_init

parser_init()
answer = int(input('are you the host?'))
if answer:
    x = host.Host('alice', 12345)
else:
    x = client.Client('bob', 'localhost', 12345)
