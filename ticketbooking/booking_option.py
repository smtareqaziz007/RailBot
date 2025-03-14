import constants as const
import time
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BookingOption:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_all_trains(self):
        # finding all the trains
        train_options = self.driver.find_elements(By.CSS_SELECTOR,
                                                  'app-trip[mode="SEARCH_RESULT"]'
                                                  )
        return train_options

    def finding_available_class_for_desired_train(self, train_option):
        # finding available classes for the desired train
        class_options = train_option.find_elements(By.CSS_SELECTOR,
                                                   'div[class="single-seat-class seat-available-wrap ng-star-inserted"]'
                                                   )

        # class_options = []

        # try:
        #     class_options = WebDriverWait(train_option, 2).until(EC.presence_of_all_elements_located((
        #         By.CSS_SELECTOR,
        #         'div[class="single-seat-class seat-available-wrap ng-star-inserted"]'
        #     )))
        # except Exception as e:
        #     print("No class found")

        for option in class_options:
            class_name = option.find_element(
                By.CLASS_NAME, "seat-class-name")
            if class_name.text in const.BLOCKED_CLASSES:
                class_options.remove(option)
                if len(class_options) == 0:
                    time.sleep(3)
                print(class_name.text + " was available but in blocked list")

        return class_options

    def get_desired_train_first(self, train_options, desired_train):
        # getting the desired train at first position
        optimal_options = []
        for opt in train_options:
            t_name = opt.find_element(By.CLASS_NAME, "ng-star-inserted")
            # print(t_name.text)
            if desired_train.upper() in t_name.text:
                optimal_options.insert(0, opt)
                continue
            if t_name.text.split()[0] not in const.BLOCKED_TRAIN:
                optimal_options.append(opt)
        return optimal_options

    def get_desired_trains(self, train_options, desired_train):
        # getting the desired train at first position
        optimal_options = []
        for opt in train_options:
            t_name = opt.find_element(By.CLASS_NAME, "ng-star-inserted")
            # print(t_name.text)
            if const.TRAIN.upper() in t_name.text:
                optimal_options.insert(0, opt)
                continue
            if t_name.text.split()[0].upper() not in const.BLOCKED_TRAIN and t_name.text.split()[0].upper() in const.TRAINS:
                optimal_options.append(opt)
        return optimal_options

    def get_desired_class_first(self, class_options, desired_class):
        # **** iterating through each class but skipping undesired classes (need to work on this) ****
        optimal_options = []
        for option in class_options:
            class_name = option.find_element(
                By.CLASS_NAME, "seat-class-name")
            # print(class_name.text)
            # if class_name.text not in const.BLOCKED_CLASSES and class_name.text not in desired_class:
            #     optimal_options.append(class_)
            if class_name.text == desired_class:
                optimal_options.insert(0, option)
            else:
                optimal_options.append(option)
        return optimal_options

    def click_book_now_button(self, class_options):
        class_name = class_options[0].find_element(
            By.CLASS_NAME, "seat-class-name")
        print(class_name.text)
        book_now_button = class_options[0].find_element(By.CSS_SELECTOR,
                                                        'button[class="book-now-btn seatsLayout"]'
                                                        )
        time.sleep(const.WAIT)
        book_now_button.click()

    def desired_train_only(self, desired_class, desired_train):

        train_options = self.get_all_trains()
        train_options = self.get_desired_train_first(
            train_options, desired_train)

        train_name = train_options[0].find_element(
            By.CLASS_NAME, "ng-star-inserted").text
        # print(f"Train name = {train_name}")
        if desired_train.upper() not in train_name:
            print(f"No train found by the name: {desired_train}")
            time.sleep(const.TIMEOUT)
            raise Exception("No train found by this name")

        class_options = self.finding_available_class_for_desired_train(
            train_options[0])

        if not class_options:
            # time.sleep(const.TIMEOUT)
            t = datetime.now()
            raise Exception("No ticket available for this train")

        class_options = self.get_desired_class_first(
            class_options, desired_class)
        self.click_book_now_button(class_options)

    def desired_class_only(self, desired_class, desired_train):
        # getting all the trains
        train_options = self.get_all_trains()

        # getting the desired train at first position
        train_options = self.get_desired_train_first(
            train_options, desired_train)

        # class options[] has available desired classes for all trains
        class_options = []
        for train in train_options:
            classes = self.finding_available_class_for_desired_train(train)
            classes = self.get_desired_class_first(classes, desired_class)
            # print(f"Classes = {classes}")
            if classes:
                class_name = classes[0].find_element(
                    By.CLASS_NAME, "seat-class-name")
                if desired_class == class_name.text:
                    class_options.append(classes[0])
            if class_options:
                break

        if not class_options:
            # time.sleep(const.TIMEOUT)
            raise Exception("Desired class from all the trains is booked")

        self.click_book_now_button(class_options)

    def desired_train_and_class_only(self, desired_class, desired_train):
        # getting all the trains
        train_options = self.get_all_trains()
        # getting desired train first
        train_options = self.get_desired_train_first(
            train_options, desired_train)

        train_name = train_options[0].find_element(
            By.CLASS_NAME, "ng-star-inserted").text
        # print(f"Train name = {train_name}")
        if desired_train.upper() not in train_name:
            print(f"No train found by this name {desired_train}")
            time.sleep(const.TIMEOUT)
            raise Exception("No train found by this name")

        class_options = self.finding_available_class_for_desired_train(
            train_options[0])

        if not class_options:
            # time.sleep(const.TIMEOUT)
            raise Exception("No ticket available for this train")

        class_options = self.get_desired_class_first(
            class_options, desired_class)
        class_name = class_options[0].find_element(
            By.CLASS_NAME, "seat-class-name")

        if class_name.text != desired_class:
            time.sleep(const.TIMEOUT)
            raise Exception("Desired class is booked")

        self.click_book_now_button(class_options)

    def desired_trains_only(self, desired_class, desired_train):

        # getting all the trains
        train_options = self.get_all_trains()

        # get only the desired trains
        train_options = self.get_desired_trains(
            train_options, desired_train)

        # for train in train_options:
        #     train_name = train.find_element(
        #         By.CLASS_NAME, "ng-star-inserted").text

        #     print(train_name)

        # finding available classes for the desired train
        class_options = self.finding_available_class_for_desired_train(
            train_options[0])

        # finding the first train that has available seats
        # ******* eikhane full wait korte hoy train a seat na thakle *******
        index = 0
        while len(class_options) == 0:
            print("aschi train change korte")
            index += 1
            if index >= len(train_options):  # all train seats are booked
                break
            class_options = self.finding_available_class_for_desired_train(
                train_options[index])
            if len(class_options) > 0:
                break

        if len(class_options) == 0:
            time.sleep(const.TIMEOUT)
            raise Exception("All trains are booked")

        class_options = self.get_desired_class_first(
            class_options, desired_class)
        self.click_book_now_button(class_options)

    def default(self, desired_class, desired_train):

        # getting all the trains
        train_options = self.get_all_trains()

        # getting the desired train at first position
        train_options = self.get_desired_train_first(
            train_options, desired_train)

        # finding available classes for the desired train
        class_options = self.finding_available_class_for_desired_train(
            train_options[0])

        # ***** here i can append the rest classes from other trains*****

        # finding the first train that has available seats
        # ******* eikhane full wait korte hoy train a seat na thakle *******
        index = 0
        while len(class_options) == 0:
            print("aschi train change korte")
            index += 1
            if index >= len(train_options):  # all train seats are booked
                break
            class_options = self.finding_available_class_for_desired_train(
                train_options[index])
            if len(class_options) > 0:
                break

        if len(class_options) == 0:
            time.sleep(const.TIMEOUT)
            raise Exception("All trains are booked")

        class_options = self.get_desired_class_first(
            class_options, desired_class)
        self.click_book_now_button(class_options)

        # items = driver.find_elements(By.CSS_SELECTOR,"div.examplenameA:not(.examplenameB)")
