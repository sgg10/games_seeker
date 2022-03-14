import click

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec

class Juegos(object):

    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._url = "https://www.3djuegos.com/novedades/juegos-generos/juegos-pc/0f1f0f0/juegos-populares/"

    @property
    def is_loaded(self):
        WebDriverWait(self._driver, 15).until(ec.presence_of_element_located((By.CLASS_NAME, "list_nov")))
        return True

    def close_popups(self, web_element):
        try:
            popup = WebDriverWait(self._driver, 5).until(web_element)
            if popup:
                popup.click()
        except:
            pass

    def close_all_popups(self):
        self.close_popups(ec.presence_of_element_located((By.ID, "didomi-notice-agree-button")))
        self.close_popups(ec.presence_of_element_located((By.ID, "cierra")))

    def open(self):
        self._driver.get(self._url)

    def get_game(self, _id):
        try:
            game = WebDriverWait(self._driver, 1).until(
                ec.presence_of_element_located(
                    (
                        By.XPATH,
                        f'//*[@id="tb926"]/div[1]/div[5]/div[2]/ul/li[{_id}]/article/div/div[2]/h2/a'
                    )

                )
            )

            return game.text, game.get_attribute("href")
        except KeyboardInterrupt:
            raise click.Abort
        except:
            return None

    def get_all_games(self):
        total_pages = 150 #int(self._driver.find_elements(by=By.CLASS_NAME, value="page_opti")[-1].text)
        games = []
        for page in range(1, total_pages + 1):
            total_items = len(self._driver.find_elements(by=By.CLASS_NAME, value="li_lin14"))

            with click.progressbar(range(1, total_items+1), label=f"Games of page {page}") as bar:
                for i in bar:
                    game = self.get_game(i)
                    if game:
                        games.append(game)

            if total_pages > 1:
                try:
                    next_button = self._driver.find_element(
                        by=By.XPATH,
                        value='//*[@id="tb926"]/div[1]/div[6]/div/div[3]/a'
                    )
                    if next_button:
                        next_button.click()
                        self.is_loaded
                except:
                    break

        return games

    def get_minimum_requirements(self, games):
        required = ("Sistema operativo", "Procesador", "Memoria", "Gráficos", "Almacenamiento")
        games_req = []
        with click.progressbar(games, label=f"Getting games requirements") as bar:
            for name, link in bar:
                try:
                    self._driver.get(link)
                    req_button = WebDriverWait(self._driver, 10).until(
                        ec.presence_of_element_located(
                            (By.XPATH, '//*[@id="tb926"]/div[1]/div[2]/div[1]/div/div/div[1]/a')
                        )
                    )
                    req_button.click()
                    WebDriverWait(self._driver, 15).until(ec.presence_of_element_located((By.CLASS_NAME, "list_foro")))
                    req_items = self._driver.find_elements(
                        by=By.XPATH,
                        value='//*[@id="tb926"]/div[1]/article/div[2]/div/div[1]/ul/li'
                    )
                except:
                    continue

                req_items = list(map(lambda r: r.text.split(":"), req_items))

                requirements = {item[0]: item[1] for item in req_items if len(item) == 2}

                games_req.append([name, link] + [requirements.get(key) for key in required])

        return games_req

