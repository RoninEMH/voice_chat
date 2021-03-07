import click
from random import randint


@click.command("Create")
@click.option('--name', '-n', required=True)
@click.option('--voice', '-v', default=randint(1000, 1500), type=int)
@click.option('--chat', '-c', default=randint(1500, 2000), type=int)
def create(name, voice, chat):
    print(f"Name : {name} Voice : {voice} Chat : {chat}")


@click.command("Join")
@click.option('--name', '-n', required=True)
@click.option('--host', '-h', required=True)
@click.option('--voice', '-v', default=randint(1000, 1500), type=int)
@click.option('--chat', '-c', default=randint(1500, 2000), type=int)
def join(name, host, voice, chat):
    print(f"Name : {name} Host : {host} Voice : {voice} Chat : {chat}")


@click.group()
def cli():
    pass


cli.add_command(create)
cli.add_command(join)
cli()
