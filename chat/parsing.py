COMMAND_PREFIX = '/'

command_dictionary = {}


def parser_init():
    def foo(*args):
        print('foo')

    def bar(*args):
        print('bar')

    def stop(*args):
        _ , connection = args
        print('stopping')
        connection.close()

    commands = [foo, bar, stop]
    for command in commands:
        command_dictionary[command.__name__] = command


def parse_command(cmd, args, connection):
    try:
        command_dictionary[cmd](args,connection)
    except KeyError:
        print('no such command.')


def parse(str, connection):
    if str.startswith(COMMAND_PREFIX):
        str = str[len(COMMAND_PREFIX):].split()  # command is the first element, args are the rest
        parse_command(str[0], str[1:],connection)
    else:
        return str
