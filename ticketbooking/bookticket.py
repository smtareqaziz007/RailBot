from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import constants as const
from ticketbooking.booking_option import BookingOption
# from ticketbooking.seat_selection import SeatSelection
from datetime import datetime
import time
import os


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=const.DRIVER_PATH, teardown=False):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("detach", True)
        # options.add_argument('--disable-extensions')
        # options.add_argument('--disable-images')
        os.environ['PATH'] += r"/usr/local/bin/chromedriver"
        # self.driver_path = driver_path
        # self.teardown = teardown

        super(Booking, self).__init__(
            executable_path=driver_path, options=options)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def refresh(self) -> None:
        return super().refresh()

    def wait_until_time(self, minute, second):
        while True:
            t = datetime.now()
            if t.minute == minute and t.second == second:
                # bot.land_first_page()
                break

    def isBrowserAlive(self):
        try:
            self.get(const.BASE_URL)
            return True
        except:
            return False

    # def my_sort_condition(self, bogie):  # not usable at this moment
    #     seat_layout = self.find_element(By.CSS_SELECTOR,
    #                                     'div[class="seat-layout"]'
    #                                     )
    #     time.sleep(const.WAIT)
    #     seats = seat_layout.find_elements(By.CSS_SELECTOR,
    #                                       'button[class="btn uppercase p-2 w-4 bg-[#F6F7F9]"]'
    #                                       )
    #     return len(seats)

    def land_first_page(self, BASE_URL):
        # print(const.DATE)
        self.maximize_window()
        self.get(BASE_URL)
        self.implicitly_wait(20)
        # time.sleep(const.WAIT)

    def land_page(self, url):
        self.get(url)

    def get_url(self):
        return self.current_url

    def change_wait(self, timeout):
        self.implicitly_wait(timeout)

    def click_agree_btn(self):
        time.sleep(1)
        agree_btn = self.find_element(By.CLASS_NAME, 'btn-agree')
        time.sleep(const.WAIT)
        agree_btn.click()
        # login_option = self.find_element_by_link_text("Login")
        # login_option.click()

    def login(self, MOBILE, PASSWORD):
        login_option = self.find_element(By.CSS_SELECTOR,
                                         'button[class="btn shadow-lg p-2 rounded-full font-bold text-sm uppercase bg-primary w-40 h-12 text-white"]'
                                         )
        login_option.click()
        mobile_num = self.find_element(By.CSS_SELECTOR,
                                       'input[placeholder="Mobile Number"]'
                                       )
        password = self.find_element(By.CSS_SELECTOR,
                                     'input[type="password"]'
                                     )

        # if const.MOBILE == "":
        #     const.MOBILE = input("Enter Mobile number: ")
        # if const.MOBILE == "":
        #     const.PASSWORD = input("Enter Password: ")

        mobile_num.send_keys(f"{MOBILE}")
        password.send_keys(f"{PASSWORD}")
        time.sleep(0.3)

        login_btn = self.find_element(By.CSS_SELECTOR,
                                      'button[type="submit"]'
                                      )
        time.sleep(0.5)
        login_btn.click()

        # os.system('spd-say "your program has finished"')
        # os.system('play -nq -t alsa synth {} sine {}'.format(1, 440))
        # print('\007')
        # print('\a')

    def fill_stations(self, from_city, to_city):
        frm = self.find_element(By.CSS_SELECTOR,
                                'app-search-input[inputtype="FROM"]'
                                )
        to = self.find_element(By.CSS_SELECTOR,
                               'app-search-input[inputtype="TO"]'
                               )

        time.sleep(const.WAIT)
        frm.click()
        frminput = self.find_element(By.CSS_SELECTOR,
                                     'input[placeholder="Type station name"]'
                                     )
        time.sleep(const.WAIT)
        frminput.send_keys(f"{from_city}")
        frmslct = self.find_elements(By.CSS_SELECTOR,
                                     'div[class="flex-1 flex items-center h-full border-b border-[#9A9BA7] station-names"]'
                                     )
        time.sleep(const.WAIT)
        frmslct[0].click()

        time.sleep(const.WAIT)

        to.click()
        toinput = self.find_element(By.CSS_SELECTOR,
                                    'input[placeholder="Type station name"]'
                                    )
        time.sleep(const.WAIT)
        toinput.send_keys(f"{to_city}")
        toslct = self.find_elements(By.CSS_SELECTOR,
                                    'div[class="flex-1 flex items-center h-full border-b border-[#9A9BA7] station-names"]'
                                    )
        time.sleep(const.WAIT)
        toslct[0].click()
        # time.sleep(0.5)

    def select_date_and_class(self, Date):
        class_option = self.find_element(By.CSS_SELECTOR,
                                         'app-search-input[inputtype="SEAT_CLASS"]'
                                         )
        time.sleep(const.WAIT)
        class_option.click()
        class_types = self.find_elements(By.CSS_SELECTOR,
                                         'app-button[class="ng-star-inserted"]'
                                         )
        time.sleep(const.WAIT)
        class_types[2].click()
        # time.sleep(0.5)

        date_option = self.find_element(By.CSS_SELECTOR,
                                        'app-search-input[inputtype="DATE"]'
                                        )
        time.sleep(const.WAIT)
        date_option.click()

        if const.today.month != const.expected_date.month:
            month_change_button = WebDriverWait(self, 1).until(EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'button[class="mat-focus-indicator overflow-hidden mat-icon-button mat-button-base"]'
            )))
            time.sleep(0.1)
            month_change_button.click()

        date = self.find_element(By.CSS_SELECTOR,
                                 f'button[aria-label="{Date}"]'
                                 )
        time.sleep(0.5)
        date.click()

    def search_trains(self):
        search = self.find_element(By.CSS_SELECTOR,
                                   'button[class="btn shadow-lg p-2 rounded-full font-bold text-sm uppercase bg-primary w-full text-white login-form-submit-btn h-12"]'
                                   )
        time.sleep(const.WAIT)
        search.click()

    def book_now(self, book_class, no_of_tickets, train_name, booking_option=1):
        ticketing_option = BookingOption(self)
        if booking_option == 1:
            ticketing_option.default(book_class, train_name)
        elif booking_option == 2:
            ticketing_option.desired_train_only(book_class, train_name)
        elif booking_option == 3:
            ticketing_option.desired_class_only(book_class, train_name)
        else:
            ticketing_option.desired_train_and_class_only(
                book_class, train_name)

        # self.book_ticket(no_of_tickets)

    def select_seat(self, no_of_tickets):
        # seat_selection_option = SeatSelection(self)
        # seat_selection_option.default(no_of_tickets)

        # firstly finding the bogie_row
        to_be_purchased = no_of_tickets
        bogie_row = self.find_element(By.CSS_SELECTOR,
                                      'div[class="mt-2 flex flex-wrap relative -ml-1 -mr-1"]'
                                      )

        bogies = WebDriverWait(bogie_row, 10).until(EC.presence_of_all_elements_located((
            By.CSS_SELECTOR,
            'button'
        )))
        # print(len(bogies))

        # time.sleep(const.WAIT)

        selected_seats = 0

        for bogie in bogies:
            try:
                if to_be_purchased == 0:
                    break

                # time.sleep(0.5)
                print(bogie.text)
                # skip the bogie that doesn't have a name
                if bogie.text == "":
                    continue
                # bogie.click()
                # actions.move_to_element(bogie).click().perform()
                # self.execute_script("arguments[0].scrollIntoView();", bogie)
                self.execute_script("arguments[0].click();", bogie)

                seat_layout = WebDriverWait(self, 10).until(EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    'div[class="seat-layout"]'
                )))

                seats = WebDriverWait(seat_layout, 3).until(EC.presence_of_all_elements_located((
                    By.CSS_SELECTOR,
                    'button[class="btn uppercase p-2 w-4 bg-[#FFFFFF] text-black border-2 border-black"]'
                )))

                # time.sleep(const.WAIT)
                print(len(seats))

                for seat in seats:
                    try:
                        if seat.text != "":
                            print(seat.text)
                            # seat.click()
                            try:
                                self.execute_script(
                                    "arguments[0].click();", seat)
                            except Exception as e:
                                print(e)
                                continue

                            # here i need to check if the selection was successful
                            no_of_selected = self.find_elements(By.CSS_SELECTOR,
                                                                'span[class="single-seat-number ng-star-inserted"]'
                                                                )

                            time.sleep(0.5)
                            no_of_selected = WebDriverWait(self, 1).until(EC.presence_of_all_elements_located((
                                By.CSS_SELECTOR,
                                'span[class="single-seat-number ng-star-inserted"]'
                            )))

                            if no_of_selected:
                                selected_seats = len(no_of_selected)
                                print(f"selected = {selected_seats}")
                                if len(no_of_selected) == no_of_tickets:
                                    to_be_purchased = 0
                                    break

                            time.sleep(0.1)

                    except Exception as e:
                        print("Error in ticket selecting")
                        print(e)

            except Exception as e:
                print("Bogie changing error occured")
                print(e)

        # self.click_confirm_purchase(selected_seats)
        return selected_seats

    def fill_passenger_name(self, passenger_list):
        try:
            name_options = self.find_elements(By.CSS_SELECTOR,
                                              'input[class="w-full h-10 block form-control border border-input-border ng-untouched ng-pristine ng-invalid"]'
                                              )
            time.sleep(const.WAIT)
            i = 0

            if len(passenger_list) < 3:
                passenger_list += [passenger_list[-1], passenger_list[-1]]
                print(passenger_list)

            for option in name_options:
                option.send_keys(f"{passenger_list[i]}")
                i += 1
                time.sleep(const.WAIT)

        except Exception as e:
            print(e)
            raise Exception("Unable to fill co-passenger/s name")

    def extract_information(self):
        try:
            trip_data = self.find_element(By.CSS_SELECTOR,
                                          'div[class="card mt-2 single-trip-card"]'
                                          )

            train_found = trip_data.find_element(By.CSS_SELECTOR,
                                                 'div[class="trip-card-header"]'
                                                 )
            # print(train_found.text)
            const.TRAIN_FOUND = train_found.text

            date_and_time = trip_data.find_element(By.CSS_SELECTOR,
                                                   'span[class="trip-card-date ng-star-inserted"]'
                                                   )
            # print(date_and_time.text)
            const.TRAIN_TIME = date_and_time.text

            data = trip_data.find_elements(By.CSS_SELECTOR,
                                           'div[ class="card-data-value ng-star-inserted"]'
                                           )
            # print(data[2].text)
            const.CLASS_FOUND = data[2].text

            seats = trip_data.find_elements(By.CSS_SELECTOR,
                                            'span[class="single-seat-number ng-star-inserted"]'
                                            )
            items = []
            for seat in seats:
                items.append(seat.text)
            const.SEATS = ' , '.join(items)

            # if (int(data[3].text) < const.NO_OF_TICKETS - 1):
            #     raise Exception("seat_error")

        except Exception as e:
            print("Unable to fetch information")
            if (str(e) == "seat_error"):
                time.sleep(const.WAIT)
                raise Exception(
                    "Number of tickets selected is less than desired")
            print(e)

    def click_confirm_purchase(self, selected_seats):
        try:
            confirm_purchase_btn = self.find_element(By.CSS_SELECTOR,
                                                     'button[class="btn shadow-lg p-2 rounded-full font-bold text-sm uppercase bg-primary text-white w-full h-12"]'
                                                     )

            time.sleep(const.WAIT)
            # confirm_purchase_btn.click()
            self.execute_script("arguments[0].click();", confirm_purchase_btn)
            time.sleep(const.WAIT)
            # self.click_proceed()

        except Exception as e:
            print("Error clicking confirm button")
            print(e)
            if selected_seats == 0:
                raise Exception("Unable to select any seat")

    def click_proceed(self):
        try:
            proceed_btn = self.find_element(By.CSS_SELECTOR,
                                            'button[class="btn shadow-lg p-2 rounded-full font-bold text-sm uppercase bg-primary w-full h-12 text-white"]'
                                            )

            time.sleep(const.WAIT)
            proceed_btn.click()
            time.sleep(const.WAIT)
            # self.select_payment_method()
        except Exception as e:
            print("Error clicking proceed button")
            print(e)

    def select_payment_method(self, payment_method="bkash"):
        try:

            if payment_method == "nagad":

                nagad = self.find_element(By.CSS_SELECTOR,
                                          'img[src="assets/images/select-payment/nagad.svg"]'
                                          )
                time.sleep(const.WAIT)
                nagad.click()

            elif payment_method == "bkash":
                bkash = self.find_element(By.CSS_SELECTOR,
                                          'img[src="assets/images/select-payment/bkash.svg"]'
                                          )  # class="image w-16"
                time.sleep(const.WAIT)
                bkash.click()

            elif payment_method == "rocket":

                rocket = self.find_element(By.CSS_SELECTOR,
                                           'img[src="assets/images/select-payment/rocket.svg"]'
                                           )
                time.sleep(const.WAIT)
                rocket.click()

            else:

                dbbl_nexus = self.find_element(By.CSS_SELECTOR,
                                               'img[src="assets/images/select-payment/nexus-debit.svg"]'
                                               )
                time.sleep(const.WAIT)
                dbbl_nexus.click()

            time.sleep(const.WAIT)

            to_payment_btn = self.find_element(By.CSS_SELECTOR,
                                               'button[class="btn shadow-lg p-2 rounded-full font-bold text-sm uppercase bg-primary w-full h-12 text-white"]'
                                               )

            time.sleep(const.WAIT)
            to_payment_btn.click()

        except Exception as e:
            print("Error selecting payment method")
            print(e)
