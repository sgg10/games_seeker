import click
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from games_seeker.scraper.Juegos.page import Juegos


@click.command("scrap-amazon")
@click.option('-o', '--output', type=str)
def cli(output):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    gp = Juegos(driver)
    gp.open()
    assert gp.is_loaded
    gp.close_all_popups()
    result = gp.get_all_games()
    result = pd.DataFrame(
        gp.get_minimum_requirements(result),
        columns=["name", "url", "Sistema operativo", "Procesador", "Memoria", "Gráficos", "Almacenamiento"]
    )
    driver.close()

    if result.shape[0]:
        if not output:
            output = f"./data/raw/{type(gp).__name__.lower()}.csv"
        result.to_csv(output, sep="|", index=False)
    else:
        click.echo(click.style("No Results", fg="red"))
