import importlib
import os

import click


class CLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir("./games_seeker/commands"):
            if filename.endswith(".py") and not filename.startswith("__"):
                rv.append(filename.replace('.py', ''))
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            mod = importlib.import_module(f".{name}", "games_seeker.commands")
        except ImportError:
            return

        if "cli" in dir(mod):
            return mod.cli
        return
