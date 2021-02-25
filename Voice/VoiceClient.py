from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import pyaudio
import queue
import threading


class VoiceClient(DatagramProtocol):
    def __init__(self, ip, port, command_queue):
        self.another_client = ip, port
        self.buffer = 1024
        self.mute = False
        self.output_stream = None
        self.input_stream = None
        self.message_queue = command_queue
        self.initialize_messages()

    def initialize_messages(self):
        self.message_to_mute = "mute"
        self.message_to_unmute = "unmute"
        self.message_to_abort = "abort"

    def startProtocol(self):
        print("starting protocol")
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
        threading.Thread(target=self.check_queue, daemon=True).start()

    def stopProtocol(self):
        print("disconnected!!!")

    def record(self):
        while not self.mute:
            data = self.input_stream.read(self.buffer)
            self.transport.write(data, self.another_client)

    def datagramReceived(self, datagram, address):
        self.output_stream.write(datagram)

    def check_queue(self):
        while True:
            if not self.message_queue.empty():
                message = self.message_queue.get()
                if message == self.message_to_mute:
                    self.mute = True
                elif message == self.message_to_unmute:
                    self.mute = False
                    reactor.callInThread(self.record)
                elif message == self.message_to_abort:
                    print("in abort now!!!")
                    self.mute = True  # just for safety
                    try:
                        self.input_stream.close()
                        self.output_stream.close()
                    except OSError:
                        print("closing connection")
                    reactor.stop()  # not in try because we want to stop anyway
                    break

    def run(self):
        reactor.listenUDP(self.another_client[1], self)
        reactor.run()
