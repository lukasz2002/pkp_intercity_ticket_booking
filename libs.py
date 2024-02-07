from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class Web:
    def __init__(self):
        # self.login = input("Pass email: ")
        # self.password = input("Pass password: ")
        self.start_station = input("Pass start station: ")
        self.destination_station = input("Pass destination station: ")
        # self.date = input("Pass date in format DD-MM-YY: ")
        # self.time = input("Pass when train should start from start station (format: HH): ")
        # self.preferred_ticket_class = input("What is your preferred class? First -> 1, Second -> 2: ")
        # self.reduced_tariff = input("Any tariff? ")
        self.driver = None

    def init_web(self):
        options = Options()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                       options=options)
        self.driver.get("https://www.intercity.pl/pl/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def pass_station_and_date(self):
        inputs = {
            'start_station': '//*[@id="stname-0"]',
            'final_station': '//*[@id="stname-1"]',
        }
        self.pass_single_station(inputs["start_station"], self.start_station)
        self.pass_single_station(inputs["final_station"], self.destination_station)

    def pass_single_station(self, input_xpath, input_value):
        input_element = self.driver.find_element(By.XPATH, input_xpath)
        input_element.clear()
        input_element.send_keys(input_value)
        input_popup_element = rf"//strong[contains(text(), '{input_value.title()}')]"
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, input_popup_element))
            )
        except TimeoutException:
            print("Wrong station provided")
            self.driver.quit()
            exit()

        ActionChains(driver=self.driver) \
            .key_down(Keys.ARROW_DOWN) \
            .key_down(Keys.ENTER) \
            .perform()
