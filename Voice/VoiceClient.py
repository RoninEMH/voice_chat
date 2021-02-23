from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import pyaudio
import queue
import threading


class Client(DatagramProtocol):
    def __init__(self, ip, port, command_queue):
        self.another_client = ip, port
        self.buffer = 1024  # 127.0.0.1
        self.mute = False
        self.output_stream = None
        self.input_stream = None
        self.message_to_mute = "mute please"
        self.message_queue = queue.SimpleQueue()
        for element in command_queue:
            self.message_queue.put(element)

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
        # reactor.callInThread(self.record)
        # not sure if needed

    def record(self):
        while not self.mute:
            data = self.input_stream.read(self.buffer)
            self.transport.write(data, self.another_client)
            if not self.message_queue.empty():
                message = self.message_queue.get()
                if message == self.message_to_mute:
                    self.Mute()

    def datagramReceived(self, datagram, address):
        self.output_stream.write(datagram)

    def Mute(self):
        self.mute = True
