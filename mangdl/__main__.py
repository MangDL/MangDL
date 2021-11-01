import click

commands = {
}

@click.group(commands=commands)
def cli():
	pass

if __name__ == '__main__':
	cli()
