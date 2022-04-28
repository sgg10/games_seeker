import click
from games_seeker.nl_controller.controller import NaturalLanguageController


@click.command()
def cli():
    nlc = NaturalLanguageController()
    result = nlc.run()
    click.clear()
    if result[1]:
        click.echo(click.style(f"Greate, your command is '{result[1]}'!", fg="green"))
    result[0]()
