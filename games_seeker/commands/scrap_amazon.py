import click
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from games_seeker.scraper.Amazon.amazon_page import Amazon


@click.command("scrap-amazon")
@click.option('-s', '--search', type=str, required=True)
@click.option('-o', '--output', type=str)
def cli(search, output):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    amz = Amazon(driver)
    amz.open()
    assert amz.is_loaded
    amz.search(search)

    query_results = pd.DataFrame(amz.get_all_products(), columns=["title", "symbol", "price", "link"])
    driver.close()

    if query_results.shape[0]:
        if not output:
            output = f"./data/raw/{type(amz).__name__.lower()}_{search.replace(' ', '_').replace('-', '_')}.csv"
        query_results.to_csv(output, sep="|", index=False)
    else:
        click.echo(click.style("No Search Results", fg="red"))
