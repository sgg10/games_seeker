import click

from games_seeker.utils.cli import CLI

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    token_normalize_func=lambda x: x.lower(),
)


@click.command(cls=CLI, context_settings=CONTEXT_SETTINGS)
def cli():
    pass


cli()
