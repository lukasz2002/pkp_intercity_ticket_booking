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
import locale
import calendar


class Web:
    def __init__(self):
        # self.login = input("Pass email: ")
        # self.password = input("Pass password: ")
        self.start_station = input("Pass start station: ")
        self.destination_station = input("Pass destination station: ")
        self.date = input("Pass date in format DD-MM-YYYY: ")
        # self.time = input("Pass when train should start from start station (format: HH): ")
        # self.preferred_ticket_class = input("What is your preferred class? First -> 1, Second -> 2: ")
        # self.reduced_tariff = input("Any tariff? ")
        self.driver = None
        self.date_as_dict = None

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
        self.remove_popup_station()

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

    def remove_popup_station(self):
        element_to_remove_by_click = '//*[@id="searchTrainForm"]/div[2]/div[1]'
        input_element = self.driver.find_element(By.XPATH, element_to_remove_by_click)
        input_element.click()

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
            if date_dict["month"] == date.today().month:
                lower_day_limit = date.today().day
                self.check_lower_date_limit(date_dict["day"], lower_day_limit, "day")
            upper_day_limit = calendar.monthrange(date_dict["year"], date_dict["month"])[1]
            self.check_upper_date_limit(date_dict["day"], upper_day_limit, "day")
        else:
            upper_month_limit = date.today().month
            self.check_upper_date_limit(date_dict["month"], upper_month_limit, "month")
            upper_day_limit = date.today().day
            self.check_upper_date_limit(date_dict["day"], upper_day_limit, "day")

        self.date_as_dict = date_dict

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

    def pass_date(self):
        date_input_trigger = self.driver.find_element(By.XPATH, '//*[@id="date_picker_trigger"]')
        date_input_trigger.click()
        self.choose_month_and_year()
        self.enter_day()

    def choose_month_and_year(self):
        user_month_name = self.number_to_month()
        user_year = self.date_as_dict["year"]

        while True:
            month_element = self.driver.find_element(By.XPATH, '//div[@class="asd__month"]/div/span[1]')
            year_element = self.driver.find_element(By.XPATH, '//div[@class="asd__month"]/div/span[2]')
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="asd__month"]/div/span[1]'))
            )
            if str(user_month_name) != str(month_element.text).lower() or str(user_year) != str(year_element.text):
                self.swipe_month("right")
            else:
                break

    def number_to_month(self):
        locale.setlocale(locale.LC_TIME, 'pl_PL')
        month_num = self.date_as_dict["month"]
        month_name = calendar.month_name[month_num]
        return month_name

    def swipe_month(self, button_direction):
        if button_direction == "left":
            dsc_string = "Move backward to switch to the previous month."
            button_xpath = rf"//div[1]/div[1]/button[@aria-label='{dsc_string}']"
        elif button_direction == "right":
            dsc_string = "Move forward to switch to the next month."
            button_xpath = rf"//div[1]/div[2]/button[@aria-label='{dsc_string}']"
        else:
            # TODO: raise error here
            return

        button_element = self.driver.find_element(By.XPATH, button_xpath)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, button_xpath))
            )
        except TimeoutException:
            print("Not possible to click arrow button")
            self.driver.quit()
            exit()
        button_element.click()

    def enter_day(self):
        path_to_button = "//div[2]/div[1]/div[2]/table/tbody/*/*/button"
        day = self.date_as_dict["day"]
        find_rule = f'[contains(text(), "{day}")]'
        button_elements = self.driver.find_elements(By.XPATH, rf'{path_to_button}{find_rule}')
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, rf'{path_to_button}{find_rule}'))
            )
        except TimeoutException:
            print("Popup with date didn't load in time")
            self.driver.quit()
            exit()

        button_elements[0].click()


