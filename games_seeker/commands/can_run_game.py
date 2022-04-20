import click
from time import sleep
from games_seeker.can_run.logic import Logic

RECOMENDATIONS = """
+ Al ingresar su procesador, ingrese de la siguiente forma:
    * i3 - i9 para Intel
    * r3 - r9 para AMD
+ Ingrese solo el numero que acompaña a su GPU RTX:
    * Si tiene una GTX 1050, ingrese 1050
+ Ingrese numeros enteros validos para el resto de los casos
"""

@click.command()
def cli():
    click.echo(click.style(RECOMENDATIONS, fg="yellow"))
    logic = Logic()
    so = int(input("Ingrese el numero correspondiente a su Windows: "))
    cpu = input("Ingrese su CPU: ")
    ram = int(input("Ingrese su cantidad de memoria RAM: "))
    gpu = int(input("Ingrese el numero correspondiente de su tarjeta grafica: "))
    st = int(input("Ingrese su almacenamiento: "))
    click.echo(
        click.style(
            "Ingresara a un modo interactivo, para salir use la tecla '0' cuando se le indique",
            fg="yellow"
        )
    )

    _exit = False
    sleep(1.5)

    while not _exit:
        games = logic.GAMES_REQUIREMENTS.iloc[:, 0].values
        games = list(map(lambda game: f"{game[0] + 1}. {game[1]}", enumerate(games)))
        games = "\n".join(games)
        click.echo_via_pager(games)
        opt = int(input("Escoja el id de un juego: "))
        result = logic.can_run_game(logic.GAMES_REQUIREMENTS.iloc[opt-1, 0], so, cpu, ram, gpu, st)
        click.clear()
        if result:
            click.echo(click.style("Felicidades, puedes correr este juego!!", fg="green"))
        else:
            click.echo(click.style("Lo sentimos, tu computador no cumple con los requerimientos", fg="red"))
        _exit = True if input("Ingrese 0 para salir o cualquier otra tecla para evaluar otro juego: ") == "0" else False
