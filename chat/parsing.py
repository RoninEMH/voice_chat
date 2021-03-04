import queue


class Parser:
    def __init__(self, command_queue):
        self.COMMAND_PREFIX = '/'
        self.command_dictionary = {}

        def mute(*args):
            command_queue.put('mute')

        def unmute(*args):
            command_queue.put('unmute')

        def abort(*args):
            _, connection = args
            command_queue.put('abort')
            connection.close()

        commands = [mute, unmute, abort]
        for command in commands:
            self.command_dictionary[command.__name__] = command

    def parse_command(self, cmd, args, connection):
        try:
            self.command_dictionary[cmd](args, connection)
        except KeyError:
            print('no such command.')

    def parse(self, str, connection):
        if str.startswith(self.COMMAND_PREFIX):
            str = str[len(self.COMMAND_PREFIX):].split()  # command is the first element, args are the rest
            self.parse_command(str[0], str[1:], connection)
        else:
            return str
