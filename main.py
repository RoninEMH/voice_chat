import click
import requests
from variables import SERVER_IP
from initialize_connection import initialize_connection_server, initialize_connection_client
from random import randint
import queue
from chat.host import Host
from chat.client import Client
from Voice.VoiceClient import VoiceClient
import threading
from Models.end_user import EndUser
import time


@click.command("Create")
@click.option("--name", "-n", required=True)
@click.option("--voice", "-v", default=randint(1000, 1500), type=int)
@click.option("--chat", "-c", default=randint(1500, 2000), type=int)
def create(name, voice, chat):
    requests.post(f"http://{SERVER_IP}:5000/Create", data={"name": name, "voice_port": voice, "chat_port": chat})
    q = queue.SimpleQueue()
    threading.Thread(target=Host, args=(name, int(chat), q)).start()
    user = initialize_connection_server()
    voice_client = VoiceClient(voice, user.ip, int(user.voice_port), q)
    voice_client.run()
    # print(f"Name : {name} Voice : {voice} Chat : {chat}")


@click.command("Join")
@click.option("--name", "-n", required=True)
@click.option("--host_name", "-h", required=True)
@click.option("--voice", "-v", default=randint(1000, 1500), type=int)
@click.option("--chat", "-c", default=randint(1500, 2000), type=int)
def join(name, host_name, voice, chat):
    # print(f"Name : {name} Host : {host_name} Voice : {voice} Chat : {chat}")
    host = requests.post(f"http://{SERVER_IP}:5000/Seek", data={"name": host_name}).json()
    me = EndUser(name=name, ip=host["ip"], chat_port=chat, voice_port=voice, host=False)
    if not initialize_connection_client(me):
        print("Server refused to connect")
        exit(1)
    q = queue.SimpleQueue()
    threading.Thread(target=Client, args=(name, host["ip"], int(host["chat_port"]), q)).start()
    voice_client = VoiceClient(voice, host["ip"], int(host["voice_port"]), q)
    voice_client.run()


@click.group()
def cli():
    pass


cli.add_command(create)
cli.add_command(join)
cli()
