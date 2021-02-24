from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import pyaudio
import queue
import threading


class VoiceClient(DatagramProtocol):
    def __init__(self, ip, port, command_queue):
        self.another_client = ip, port
        self.buffer = 1024  # 127.0.0.1
        self.mute = False
        self.output_stream = None
        self.input_stream = None
        self.message_queue = command_queue
        self.initialize_messages()

    def initialize_messages(self):
        self.message_to_mute = "mute please"
        self.message_to_abort = "abort please"

    def startProtocol(self):
        py_audio = pyaudio.PyAudio()

        self.output_stream = py_audio.open(
            format=pyaudio.paInt16,
            output=True,
            rate=44100,
            channels=2,
            frames_per_buffer=self.buffer,
        )
        self.input_stream = py_audio.open(
            format=pyaudio.paInt16,
            input=True,
            rate=44100,
            channels=2,
            frames_per_buffer=self.buffer,
        )
        reactor.callInThread(self.record)
        self.pull_from_queue()

    def record(self):
        while not self.mute:
            data = self.input_stream.read(self.buffer)
            self.transport.write(data, self.another_client)

    def datagramReceived(self, datagram, address):
        self.output_stream.write(datagram)

    def Mute(self):
        self.mute = True

    def check_queue(self):
        while True:
            if not self.message_queue.empty():
                message = self.message_queue.get()
                if message == self.message_to_mute:
                    self.Mute()
                if message == self.message_to_abort:
                    self.Mute()  # just for safety
                    break

    def pull_from_queue(self):
        threading.Thread(target=self.check_queue(), args=(), daemon=True)


def run(ip, port, messages_queue):
    reactor.listenUDP(port, VoiceClient(ip, port, messages_queue))
    reactor.run()
