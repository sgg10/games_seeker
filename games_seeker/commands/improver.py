import click

from games_seeker.components_improver.improver import Improver


@click.command()
def cli():
    message = """Siga las instrucciones.

        + Para CPU: Ingrese el modelo, generación y serie de esta forma -> 3-11-U
            * Recuerde que los modelos disponibles son: [3, 5, 7, 9]
            * Recuerde que las generaciones son: [5-12]
            * Recuerde que las series son: [U, B, H, K, Z, X]

        + Para RAM: ingresar solo valores numericos
        """
    click.echo(click.style(message, fg="yellow"))

    data = {
        "cpu": click.prompt("CPU"),
        "ram": click.prompt("RAM"),
        "query_type": click.prompt("speed/performance")
    }

    improver = Improver()
    click.echo(improver.query(**data))
