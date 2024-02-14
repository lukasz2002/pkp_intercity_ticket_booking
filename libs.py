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
from datetime import date
import calendar


class Web:
    def __init__(self):
        # self.login = input("Pass email: ")
        # self.password = input("Pass password: ")
        # self.start_station = input("Pass start station: ")
        # self.destination_station = input("Pass destination station: ")
        self.date = input("Pass date in format DD-MM-YYYY: ")
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

    def pass_station(self):
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

    def get_user_date_into_dict(self):
        date_as_list = self.date.split("-")
        if len(date_as_list) != 3:
            # TODO: raise error here
            print("Wrong date format")
            exit()

        for piece_of_date in date_as_list:
            if not piece_of_date.isdigit():
                # TODO: raise error here
                print("Letters were used!")
                exit()

        date_dict = {
            "day": int(date_as_list[0]),
            "month": int(date_as_list[1]),
            "year": int(date_as_list[2]),
        }

        lower_year_limit = date.today().year
        upper_year_limit = date.today().year + 1
        self.check_lower_date_limit(date_dict["year"], lower_year_limit, "year")
        self.check_upper_date_limit(date_dict["year"], upper_year_limit, "year")

        is_current_year = date_dict["year"] == lower_year_limit

        if is_current_year:
            lower_month_limit = date.today().month
            upper_month_limit = 12
            self.check_lower_date_limit(date_dict["month"], lower_month_limit, "month")
            self.check_upper_date_limit(date_dict["month"], upper_month_limit, "month")
            lower_day_limit = date.today().day
            upper_day_limit = calendar.monthrange(date_dict["year"], date_dict["month"])[1]
            self.check_lower_date_limit(date_dict["day"], lower_day_limit, "day")
            self.check_upper_date_limit(date_dict["day"], upper_day_limit, "day")
        else:
            upper_month_limit = date.today().month
            self.check_upper_date_limit(date_dict["month"], upper_month_limit, "month")
            upper_day_limit = date.today().day
            self.check_upper_date_limit(date_dict["day"], upper_day_limit, "day")

        return date_dict

    @staticmethod
    def check_upper_date_limit(user_date, limit, msg):
        if user_date > limit:
            # TODO: raise error here
            print(f"Provided {msg} is too large!")
            exit()

    @staticmethod
    def check_lower_date_limit(user_date, limit, msg):
        if user_date < limit:
            # TODO: raise error here
            print(f"Provided {msg} is too small!")
            exit()
