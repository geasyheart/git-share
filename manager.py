import click
from app import create_app

app = create_app()


@click.group()
def commands():
    """
        定义命令...
    :return: 
    """
    pass


@commands.command()
@click.option("--reloader/--no-reloader", default=True, help="重载")
@click.option("--debug/--no-debug", default=True, help="DEBUG")
@click.option("--host", default="127.0.0.1", help="host")
@click.option("--port", default=5000, help="port")
def runserver(reloader, debug, host, port):
    """
    运行server
    :param reloader: 
    :param debug: 
    :param host: 
    :param port: 
    :return: 
    """
    app.run(use_reloader=reloader, debug=debug, host=host, port=port)


HELP = """

run server..

"""

manager = click.CommandCollection(help=HELP)

manager.add_source(commands)

if __name__ == "__main__":
    manager()
