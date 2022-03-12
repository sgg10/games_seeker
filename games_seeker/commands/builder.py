import click

from games_seeker.pc_builder.genetic_search import GeneticSearch

@click.command()
@click.option('-b', '--budget', prompt=True, type=int)
@click.option("-a", "--advance", is_flag=True, default=False)
@click.option("-n", "--number-results", type=int, default=3)
@click.option("-i", "--iterations", type=int, default=10)
def cli(budget, advance, number_results, iterations):
    cases = [{"CXPB":0.8, "MUTPB":0.2, "NGEN":50, "NIND":100}]

    if advance:
        click.echo(click.style(
                "Advanced mode will take more time to search but gives a better result (approximately 2.5 minutes)",
                fg="yellow"
            )
        )
        cases += [
            {"CXPB": 0.4, "MUTPB": 0.6, "NGEN": 50, "NIND": 100},
            {"CXPB": 0.2, "MUTPB": 0.2, "NGEN": 50, "NIND": 100},
            {"CXPB": 0.3, "MUTPB": 0.7, "NGEN": 50, "NIND": 100},
            {"CXPB": 0.6, "MUTPB": 0.4, "NGEN": 50, "NIND": 100},
        ]

    gs = GeneticSearch(budget)

    results, _ = gs.run(cases, {"iterations": iterations})

    output = [
        gs.PRODUCTS.iloc[result, :]
        for result in results.iloc[:number_results, 7]
    ]

    print(output)

