import ticketbooking.constants as const
import time
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver

class BookingOption:
    def __init__(self , driver:WebDriver):
        self.driver = driver

    def get_all_trains(self):
        # finding all the trains
        train_options = self.driver.find_elements_by_css_selector(
            'app-trip[mode="SEARCH_RESULT"]'
        )
        return train_options

    def finding_available_class_for_desired_train(self , train_option):
        # finding available classes for the desired train
        class_options = train_option.find_elements_by_css_selector(
            'div[class="single-seat-class seat-available-wrap ng-star-inserted"]'
        )

        return class_options

    def get_desired_train_first(self , train_options , desired_train):
        # getting the desired train at first position
        index = 0
        for opt in train_options:
            t_name = opt.find_element_by_class_name("ng-star-inserted")
            print(t_name.text)
            if desired_train.upper() in t_name.text:
                train_options[0], train_options[index] = train_options[index], train_options[0]
                break
            index = index + 1
        return train_options

    def get_desired_class_first(self , class_options , desired_class):
        # **** iterating through each class but skipping undesired classes (need to work on this) ****
        idx = 0
        while True:
            if idx >= len(class_options):
                break
            class_name = class_options[idx].find_element_by_class_name("seat-class-name")
            # print(class_name.text)
            if class_name.text == desired_class:
                class_options[0], class_options[idx] = class_options[idx], class_options[0]
                break
            elif class_name.text == "AC_B" or class_name.text == "AC_S":
                if idx == len(class_options) - 1:
                    break
                # putting cabins at last position
                class_options[-1], class_options[idx] = class_options[idx], class_options[-1]
                continue

            idx += 1
        return class_options

    def click_book_now_button(self , class_options):
        # while True:
        #     t = datetime.now()
        #     if t.minute == 59 and t.second == 42:
        #         break
        class_name = class_options[0].find_element_by_class_name("seat-class-name")
        print(class_name.text)
        book_now_button = class_options[0].find_element_by_css_selector(
            'button[class="book-now-btn seatsLayout"]'
        )
        time.sleep(const.WAIT)
        book_now_button.click()

    def desired_train_only(self , desired_class , desired_train):

        train_options = self.get_all_trains()
        train_options = self.get_desired_train_first(train_options , desired_train)

        train_name = train_options[0].find_element_by_class_name("ng-star-inserted").text.split()
        # print(f"Train name = {train_name}")
        if desired_train.upper() != train_name[0]:
            print(f"No train found by the name: {desired_train}")
            time.sleep(const.TIMEOUT)
            raise Exception("No train found by this name")

        class_options = self.finding_available_class_for_desired_train(train_options[0])

        if not class_options:
            # time.sleep(const.TIMEOUT)
            raise Exception("No ticket available for this train")

        class_options = self.get_desired_class_first(class_options, desired_class)
        self.click_book_now_button(class_options)



    def desired_class_only(self , desired_class , desired_train):
        # getting all the trains
        train_options = self.get_all_trains()

        # getting the desired train at first position
        train_options = self.get_desired_train_first(train_options, desired_train)


        # class options[] has available desired classes for all trains
        class_options = []
        for train in train_options:
            classes = self.finding_available_class_for_desired_train(train)
            classes = self.get_desired_class_first(classes , desired_class)
            # print(f"Classes = {classes}")
            if classes:
                class_name = classes[0].find_element_by_class_name("seat-class-name")
                if desired_class == class_name.text:
                    class_options.append(classes[0])
            if class_options:
                break

        if not class_options:
            # time.sleep(const.TIMEOUT)
            raise Exception("Desired class from all the trains is booked")

        self.click_book_now_button(class_options)

    def desired_train_and_class_only(self , desired_class , desired_train):
        # getting all the trains
        train_options = self.get_all_trains()
        # getting desired train first
        train_options = self.get_desired_train_first(train_options, desired_train)

        train_name = train_options[0].find_element_by_class_name("ng-star-inserted").text.split()
        # print(f"Train name = {train_name}")
        if  desired_train.upper() != train_name[0]:
            print(f"No train found by this name {desired_train}")
            time.sleep(const.TIMEOUT)
            raise Exception("No train found by this name")

        class_options = self.finding_available_class_for_desired_train(train_options[0])

        if not class_options:
            # time.sleep(const.TIMEOUT)
            raise Exception("No ticket available for this train")

        class_options = self.get_desired_class_first(class_options, desired_class)
        class_name = class_options[0].find_element_by_class_name("seat-class-name")

        if class_name.text != desired_class:
            time.sleep(const.TIMEOUT)
            raise Exception("Desired class is booked")

        self.click_book_now_button(class_options)


    def default(self , desired_class , desired_train):
        # getting all the trains
        train_options = self.get_all_trains()

        # getting the desired train at first position
        train_options = self.get_desired_train_first(train_options , desired_train)

        # finding available classes for the desired train
        class_options = self.finding_available_class_for_desired_train(train_options[0])

        # ***** here i can append the rest classes from other trains*****

        # finding the first train that has available seats
        # ******* eikhane full wait korte hoy train a seat na thakle *******
        index = 0
        while len(class_options) == 0:
            print("aschi train change korte")
            index += 1
            if index >= len(train_options):  # all train seats are booked
                break
            class_options = self.finding_available_class_for_desired_train(train_options[index])
            if len(class_options) > 0:
                break

        if len(class_options) == 0:
            time.sleep(const.TIMEOUT)
            raise Exception("All trains are booked")

        class_options = self.get_desired_class_first(class_options , desired_class)
        self.click_book_now_button(class_options)

        # items = driver.find_elements_by_css_selector("div.examplenameA:not(.examplenameB)")






# # finding all the trains
# train_options = self.driver.find_elements_by_css_selector(
#     'app-trip[mode="SEARCH_RESULT"]'
# )
#
# # getting the desired train at first position
# index = 0
# for opt in train_options:
#     t_name = opt.find_element_by_class_name("ng-star-inserted")
#     print(t_name.text)
#     if train_name.upper() in t_name.text:
#         train_options[0], train_options[index] = train_options[index], train_options[0]
#         break
#     index = index + 1
#
# # finding available classes for the desired train
# options = train_options[0].find_elements_by_css_selector(
#     'div[class="single-seat-class seat-available-wrap ng-star-inserted"]'
# )
#
# # ***** here i can append the rest classes from other trains*****
#
# # finding the first train that has available seats
# # ******* eikhane full wait korte hoy train a seat na thakle *******
# index = 0
# while len(options) == 0:
#     print("aschi train change korte")
#     index += 1
#     if index >= len(train_options):  # all train seats are booked
#         break
#     options = train_options[index].find_elements_by_css_selector(
#         'div[class="single-seat-class seat-available-wrap ng-star-inserted"]'
#     )
#     if len(options) > 0:
#         break
#
# # **** iterating through each class but skipping undesired classes (need to work on this) ****
# idx = 0
# while True:
#     if idx >= len(options):
#         break
#     class_name = options[idx].find_element_by_class_name("seat-class-name")
#     # print(class_name.text)
#     if class_name.text == book_class:
#         options[0], options[idx] = options[idx], options[0]
#         break
#     idx += 1
#
# for option in options:
#     class_name = option.find_element_by_class_name("seat-class-name")
#     print(class_name.text)
#     try:
#         online_seats = option.find_element_by_class_name("online-seats")
#     except:
#         online_seats = option.find_element_by_class_name("combined-seats-count")
#     print(online_seats.text)
#
#     # finding book now button for desired class
#     if online_seats.text != "0":  # it should be  >= no_of_tickets
#         book_now_button = option.find_element_by_css_selector(
#             'button[class="book-now-btn seatsLayout"]'
#         )
#         time.sleep(const.WAIT)
#         book_now_button.click()
#         # self.book_ticket(no_of_tickets)
#         break
#
#     # items = driver.find_elements_by_css_selector("div.examplenameA:not(.examplenameB)")
