import constants as const
import time
from selenium.webdriver.remote.webdriver import WebDriver


class SeatSelection:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def select_window_seats(self, no_of_tickets):
        pass

    def select_lower_seat_in_ac_berth(self, no_of_tickets):
        pass

    def select_seats_from_same_bogie(self, no_of_tickets):
        pass

    def select_two_seated_ac_berth(self, no_of_tickets):
        pass

    def select_from_two_column_seats(self, no_of_tickets):
        pass

    def default(self, no_of_tickets):
        pass
