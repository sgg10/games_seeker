from datetime import datetime

import click
import numpy as np
from docxtpl import DocxTemplate

from games_seeker.pc_builder.genetic_search import GeneticSearch


def generate_report(context, budget):
    template = DocxTemplate("templates/template_builder.docx")
    template.render(context)
    date = datetime.now().strftime("%d-%m-%Y")
    template.save(f"reports/builder_result_{budget}_{date}.docx")


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

    output = [gs.PRODUCTS.loc[result, gs.PRODUCT_INFO] for result in results.iloc[:number_results, 7]]
    output = list(map(lambda x: {
        "rows": list(map(lambda val: list(val), x.values)),
        "headers": [h.upper() for h in x.columns],
        "total": np.sum(x["price"].values)}, output)
    )

    context = {
        "results": output,
        "date": datetime.now().strftime("%d-%m-%Y %H:%M")
    }

    generate_report(context, budget)

    click.echo(click.style("✅ Report was created successfully ✅", fg="green"))
