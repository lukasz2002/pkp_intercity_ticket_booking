from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


class Web:
    def __init__(self):
        # self.login = input("Pass email: ")
        # self.password = input("Pass password: ")
        # self.start_station = input("Pass start station: ")
        # self.destination_station = input("Pass destination station: ")
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

# //*[@id="stname-0"]
# //*[@id="stname-1"]
    def pass_station_and_date(self):
        start_station_input = self.driver.find_element(By.XPATH, '//*[@id="stname-0"]')
        start_station_input.send_keys(self.start_station)
