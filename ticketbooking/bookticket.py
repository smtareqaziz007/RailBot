from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ticketbooking.constants as const
from ticketbooking.booking_option import BookingOption
# from ticketbooking.seat_selection import SeatSelection
import time


class Booking(webdriver.Chrome):
    def __int__(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        super(Booking, self).__init__()
        # os.environ['PATH'] += r"/home/smtareqaziz007/PycharmProjects/chromedriver_linux64/chromedriver"

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def isBrowserAlive(self):
        try:
            self.get(const.BASE_URL)
            return True
        except:
            return False

    def my_sort_condition(self , bogie): # not usable at this moment
        seat_layout = self.find_element_by_css_selector(
            'div[class="seat-layout"]'
        )
        time.sleep(const.WAIT)
        seats = seat_layout.find_elements_by_css_selector(
            'button[class="btn uppercase p-2 w-4 bg-[#F6F7F9]"]'
        )
        return len(seats)

    def land_first_page(self):
        # print(const.DATE)
        self.maximize_window()
        self.get(const.BASE_URL)
        self.implicitly_wait(20)
        # time.sleep(const.WAIT)

    def land_page(self , url):
        self.get(url)

    def get_url(self):
        return self.current_url

    def change_wait(self , timeout):
        self.implicitly_wait(timeout)

    def click_agree_btn(self):
        time.sleep(1)
        agree_btn = self.find_element_by_class_name('btn-agree')
        time.sleep(const.WAIT)
        agree_btn.click()
        # login_option = self.find_element_by_link_text("Login")
        # login_option.click()

    def login(self):
        login_option = self.find_element_by_css_selector(
            'button[class="btn shadow-lg p-2 rounded-full font-bold text-sm uppercase bg-primary w-40 h-12 text-white"]'
        )
        login_option.click()
        mobile_num = self.find_element_by_css_selector(
            'input[placeholder="Mobile Number"]'
        )
        password = self.find_element_by_css_selector(
            'input[type="password"]'
        )

        # if const.MOBILE == "":
        #     const.MOBILE = input("Enter Mobile number: ")
        # if const.MOBILE == "":
        #     const.PASSWORD = input("Enter Password: ")

        mobile_num.send_keys(f"{const.MOBILE}")
        password.send_keys(f"{const.PASSWORD}")
        time.sleep(0.3)

        login_btn = self.find_element_by_css_selector(
            'button[type="submit"]'
        )
        time.sleep(0.5)
        login_btn.click()

    def fill_stations(self, from_city, to_city):
        frm = self.find_element_by_css_selector(
            'app-search-input[inputtype="FROM"]'
        )
        to = self.find_element_by_css_selector(
            'app-search-input[inputtype="TO"]'
        )

        time.sleep(const.WAIT)
        frm.click()
        frminput = self.find_element_by_css_selector(
            'input[placeholder="Type station name"]'
        )
        time.sleep(const.WAIT)
        frminput.send_keys(f"{from_city}")
        frmslct = self.find_elements_by_css_selector(
            'div[class="flex-1 flex items-center h-full border-b border-[#9A9BA7] station-names"]'
        )
        time.sleep(const.WAIT)
        frmslct[0].click()

        time.sleep(const.WAIT)

        to.click()
        toinput = self.find_element_by_css_selector(
            'input[placeholder="Type station name"]'
        )
        time.sleep(const.WAIT)
        toinput.send_keys(f"{to_city}")
        toslct = self.find_elements_by_css_selector(
            'div[class="flex-1 flex items-center h-full border-b border-[#9A9BA7] station-names"]'
        )
        time.sleep(const.WAIT)
        toslct[0].click()
        # time.sleep(0.5)

    def select_date_and_class(self , Date):
        class_option = self.find_element_by_css_selector(
            'app-search-input[inputtype="SEAT_CLASS"]'
        )
        time.sleep(const.WAIT)
        class_option.click()
        class_types = self.find_elements_by_css_selector(
            'app-button[class="ng-star-inserted"]'
        )
        time.sleep(const.WAIT)
        class_types[2].click()
        # time.sleep(0.5)

        date_option = self.find_element_by_css_selector(
            'app-search-input[inputtype="DATE"]'
        )
        time.sleep(const.WAIT)
        date_option.click()

        if const.today.month != const.expected_date.month:
            month_change_button = WebDriverWait(self , 1).until(EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'button[class="mat-focus-indicator overflow-hidden mat-icon-button mat-button-base"]'
            )))
            time.sleep(0.1)
            month_change_button.click()

        date = self.find_element_by_css_selector(
            f'button[aria-label="{Date}"]'
        )
        time.sleep(0.5)
        date.click()

    def search_trains(self):
        search = self.find_element_by_css_selector(
            'button[class="btn shadow-lg p-2 rounded-full font-bold text-sm uppercase bg-primary w-full text-white login-form-submit-btn h-12"]'
        )
        time.sleep(const.WAIT)
        search.click()

    def book_now(self, book_class, no_of_tickets, train_name):
        ticketing_option = BookingOption(self)
        # ticketing_option.default(book_class , train_name)
        # ticketing_option.desired_train_only(book_class , train_name)
        ticketing_option.desired_train_and_class_only(book_class , train_name)
        # ticketing_option.desired_class_only(book_class , train_name)
        self.book_ticket(no_of_tickets)


    def book_ticket(self, no_of_tickets):
        # seat_selection_option = SeatSelection(self)
        # seat_selection_option.default(no_of_tickets)

        # firstly finding the bogie_row
        to_be_purchased = no_of_tickets
        bogie_row = self.find_element_by_css_selector(
            'div[class="mt-2 flex flex-wrap relative -ml-1 -mr-1"]'
        )

        # finding the bogies of a particular class
        # *******  eikhane full wait korte hoy prothom ta bad e faka bogey na thakle ********

        # bogies = bogie_row.find_elements_by_css_selector(
        #     'button[class="btn uppercase p-2 w-4 bg-[#F6F7F9]"]'
        # )

        # bogies = WebDriverWait(bogie_row , 1).until(EC.presence_of_all_elements_located((
        #     By.CSS_SELECTOR,
        #     'button[class="btn uppercase p-2 w-4 bg-[#F6F7F9]"]'
        # )))
        #
        # # print(f"length = {len(bogies)}")
        # # finding the defaultly selected bogie
        # first_bogie = bogie_row.find_element_by_css_selector(
        #     'button[class="btn uppercase p-2 w-4 bg-primary text-white"]'
        # )
        #
        # bogies.append(first_bogie)

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

                # time.sleep(const.WAIT)
                # seat_layout = self.find_element_by_css_selector(
                #     'div[class="seat-layout"]'
                # )

                seat_layout = WebDriverWait(self, 10).until(EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    'div[class="seat-layout"]'
                )))

                # seats = seat_layout.find_elements_by_css_selector(
                #     'button[class="btn uppercase p-2 w-4 bg-[#F6F7F9]"]'
                # )

                seats = WebDriverWait(seat_layout, 10).until(EC.presence_of_all_elements_located((
                    By.CSS_SELECTOR,
                    'button[class="btn uppercase p-2 w-4 bg-[#F6F7F9]"]'
                )))

                # time.sleep(const.WAIT)

                for seat in seats:
                    try:
                        if seat.text != "":
                            print(seat.text)
                            # seat.click()
                            try:
                                self.execute_script("arguments[0].click();", seat)
                            except Exception as e:
                                print(e)
                                continue

                            # here i need to check if the selection was successful
                            # no_of_selected = self.find_elements_by_css_selector(
                            #     'span[class="single-seat-number ng-star-inserted"]'
                            # )

                            # time.sleep(0.5)
                            # no_of_selected = WebDriverWait(self , 1).until(EC.presence_of_all_elements_located((
                            #     By.CSS_SELECTOR ,
                            #     'span[class="single-seat-number ng-star-inserted"]'
                            # )))
                            #
                            # if no_of_selected:
                            #     selected_seats = len(no_of_selected)
                            #     print(f"selected = {selected_seats}")
                            #     if len(no_of_selected) == no_of_tickets:
                            #         to_be_purchased = 0
                            #         break
                            time.sleep(0.1)
                    except Exception as e:
                        print("Error in ticket selecting")
                        print(e)

            except Exception as e:
                print("Bogie changing error occured")
                print(e)

        self.click_confirm_purchase(selected_seats)

    def click_confirm_purchase(self , selected_seats):
        try:
            confirm_purchase_btn = self.find_element_by_css_selector(
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
            proceed_btn = self.find_element_by_css_selector(
                'button[class="btn shadow-lg p-2 rounded-full font-bold text-sm uppercase bg-primary w-full h-12 text-white"]'
            )

            time.sleep(const.WAIT)
            proceed_btn.click()
            time.sleep(const.WAIT)
            self.select_payment_method()
        except Exception as e:
            print("Error clicking proceed button")
            print(e)

    def select_payment_method(self):
        try:
            bkash = self.find_element_by_css_selector(
                'img[src="assets/images/select-payment/bkash.svg"]'
            )  # class="image w-16"

            rocket = self.find_element_by_css_selector(
                'img[src="assets/images/select-payment/rocket.svg"]'
            )

            nagad = self.find_element_by_css_selector(
                'img[src="assets/images/select-payment/nagad.svg"]'
            )

            time.sleep(const.WAIT)
            rocket.click()
            time.sleep(const.WAIT)

            to_payment_btn = self.find_element_by_css_selector(
                'button[class="btn shadow-lg p-2 rounded-full font-bold text-sm uppercase bg-primary w-full h-12 text-white"]'
            )

            time.sleep(const.WAIT)
            to_payment_btn.click()

        except Exception as e:
            print("Error selecting payment method")
            print(e)

