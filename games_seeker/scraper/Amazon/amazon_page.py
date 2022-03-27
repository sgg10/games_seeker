import click

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec


class Amazon(object):

    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._url = "https://www.amazon.com/"

    @property
    def is_loaded(self):
        WebDriverWait(self._driver, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, "nav-search-field"))
            or ec.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
        return True

    def open(self):
        self._driver.get(self._url)

    def type_search(self, keyword):
        input_field = self._driver.find_element(by=By.ID, value="twotabsearchtextbox")
        input_field.send_keys(keyword)

    def click_submit(self):
        input_field = self._driver.find_element(by=By.ID, value="nav-search-submit-button")
        input_field.submit()

    def search(self, keyword):
        self.type_search(keyword)
        self.click_submit()

    def get_product(self, _id):
        try:
            label = WebDriverWait(self._driver, 5).until(
                ec.presence_of_element_located(
                    (
                        By.XPATH,
                        f'//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[{_id}]//h2/a/span'
                    )
                )
            )
            link = WebDriverWait(self._driver, 5).until(
                ec.presence_of_element_located(
                    (
                        By.XPATH,
                        f'//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[{_id}]//h2/a'
                    )
                )
            )
            symbol = WebDriverWait(self._driver, 5).until(
                ec.presence_of_element_located(
                    (
                        By.XPATH,
                        f'//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[{_id}]//span[@class="a-price-symbol"]'
                    )
                )
            )
            price = WebDriverWait(self._driver, 5).until(
                ec.presence_of_element_located(
                    (
                        By.XPATH,
                        f'//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[{_id}]//span[@class="a-price-whole"]'
                    )
                )
            )

            return label.text, symbol.text, price.text, link.get_attribute("href")
        except KeyboardInterrupt:
            raise click.Abort
        except:
            return None

    def get_all_products(self):
        total_pages = int(self._driver.find_elements(by=By.CLASS_NAME, value="s-pagination-item")[-2].text)
        data = []
        for page in range(1, total_pages + 1):
            total_items = len(self._driver.find_elements(by=By.CLASS_NAME, value="s-card-container"))

            with click.progressbar(range(total_items + 1), label=f"Items of page {page}") as bar:
                for i in bar:
                    product = self.get_product(i)
                    if product:
                        data.append(product)

            next_button = self._driver.find_element(by=By.CLASS_NAME, value="s-pagination-next")
            if next_button.get_attribute("aria-disabled") != "true":
                next_button.click()
                WebDriverWait(self._driver, 15).until(
                    ec.presence_of_all_elements_located((By.CLASS_NAME, "s-card-container"))
                )
        return data
