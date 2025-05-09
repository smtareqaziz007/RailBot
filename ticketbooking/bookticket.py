from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import constants as const
from ticketbooking.booking_option import BookingOption
from selenium.common import exceptions
# from ticketbooking.seat_selection import SeatSelection
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
from datetime import datetime
import time
import os
import signal


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=const.DRIVER_PATH, teardown=False):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        # options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("detach", True)
        # options.add_argument('--disable-extensions')
        # options.add_argument('--disable-images')
        os.environ['PATH'] += r"/usr/local/bin/chromedriver"
        # self.driver_path = driver_path
        # self.teardown = teardown

        super(Booking, self).__init__(options=options)

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

    def generate_urls(self, url):

        parsed_url = urlparse(url)

        urls = []

        # Get the query parameters as a dictionary
        query_params = parse_qs(parsed_url.query)
        for fromcity in const.FROMLIST:
            for tocity in const.TOLIST:
                for doj in const.DATELIST:

                    # Modify the value of specific parameter
                    if len(const.FROMLIST) > 1:
                        query_params['fromcity'] = [fromcity]
                    if len(const.TOLIST) > 1:
                        query_params['tocity'] = [tocity]
                    if len(const.DATELIST) > 1:
                        query_params['doj'] = [doj]

                    query_params['fromcity'] = [fromcity]
                    query_params['tocity'] = [tocity]

                    # Encode the modified query parameters
                    encoded_query = urlencode(query_params, doseq=True)

                    # Create the modified URL
                    page_url = urlunparse(
                        parsed_url._replace(query=encoded_query))
                    urls.append(page_url)
                    # print(page_url)

        return urls

    def land_first_page(self, BASE_URL):
        # print(const.DATE)
        self.maximize_window()
        self.get(BASE_URL)
        self.implicitly_wait(30)
        # time.sleep(const.WAIT)
        print("Landed on railway page")

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

        print("Logged in...")

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
        class_types[6].click()
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

        print("Necessary information filled...")

    def book_now(self):
        ticketing_option = BookingOption(self)
        if const.BOOK_NOW_OPTION == 1:
            ticketing_option.default(const.CLASS, const.TRAIN)
        elif const.BOOK_NOW_OPTION == 2:
            ticketing_option.desired_train_only(const.CLASS, const.TRAIN)
        elif const.BOOK_NOW_OPTION == 3:
            ticketing_option.desired_class_only(const.CLASS, const.TRAIN)
        elif const.BOOK_NOW_OPTION == 4:
            ticketing_option.desired_train_and_class_only(
                const.CLASS, const.TRAIN)

        else:
            ticketing_option.desired_trains_only(const.CLASS, const.TRAINS)

        # self.book_ticket(no_of_tickets)

    def get_available_bogies(self, bogie_row):
        
        # bogie_row = WebDriverWait(self, 10).until(
        #             EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="mt-2 flex flex-wrap relative -ml-1 -mr-1"]'))
        # )
        
        try:
            bogies = WebDriverWait(bogie_row, 0.7).until(EC.presence_of_all_elements_located((
            By.CSS_SELECTOR,
            'button[class="btn uppercase p-2 w-4 bg-[#FFFFFF] text-black border-2 border-black"]'
            )))
            return bogies
        except:
            first_bogie = WebDriverWait(bogie_row, 0.5).until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            'button'
            )))
            return [first_bogie]
        
    def select_seat(self, no_of_tickets):
        
        to_be_purchased = no_of_tickets
        
        bogie_row = WebDriverWait(self, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="mt-2 flex flex-wrap relative -ml-1 -mr-1"]'))
        )
        
        bogies = self.get_available_bogies(bogie_row)

        bogie_count = len(bogies)
        print("Bogies Length = " + str(bogie_count))

        selected_seats = 0

        for i in range(bogie_count - 1, -1, -1):
            try:
                if to_be_purchased == 0:
                    break
                
                bogie = bogies[i]
                print(bogie.text)
                
                self.execute_script("arguments[0].click();", bogie)

                seat_layout = WebDriverWait(self, 1).until(EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    'div[class="seat-layout"]'
                )))

                seats = WebDriverWait(seat_layout, 0.3).until(EC.presence_of_all_elements_located((
                    By.CSS_SELECTOR,
                    'button[class="btn uppercase p-2 w-4 bg-[#FFFFFF] text-black border-2 border-black"]'
                )))

                print("Seat Length = " + str(len(seats)))

                for seat in reversed(seats):
                    try:
                        if seat.text != "":
                            print(seat.text)
                            try:
                                self.execute_script(
                                    "arguments[0].click();", seat)
                            except Exception as e:
                                # print(e)
                                continue

                            no_of_selected = 0
                            time.sleep(0.3) # --------> I Have chnaged the wait from 0.5 to 0.2

                            # try: # this checking is not required while purchasing eid ticket

                            #     # here i need to check if the selection was successful
                            #     no_of_selected = WebDriverWait(self, 1).until(EC.presence_of_all_elements_located((
                            #         By.CSS_SELECTOR,
                            #         'span[class="single-seat-number ng-star-inserted"]'
                            #     )))
                            # except Exception as e:
                            #     print("Seat counting error")

                            # if no_of_selected:
                            #     selected_seats = len(no_of_selected)
                            #     print(f"selected = {selected_seats}")
                            #     if selected_seats == no_of_tickets:
                            #         to_be_purchased = 0
                            #         break
                            # 
                            # time.sleep(0.1)

                    except Exception as e:
                        print("Error in ticket selecting")
                        # print(e)

                bogies = self.get_available_bogies(bogie_row)   
            
            except exceptions.StaleElementReferenceException as e:
                bogies = self.get_available_bogies(bogie_row)
                print("Stale Element")
                bogie = bogies[i]
                print(bogie.text)
                self.execute_script("arguments[0].click();", bogie)
            except Exception as e:
                print("This bogie doesn't have any available tickets")
                # print(e)
                
        # if(selected_seats < const.NO_OF_TICKETS):
        #     raise Exception("Ticket quota not met")

        return selected_seats

    def timeout_handler(signum, frame):
        print("Timeout reached. Exiting.")
        raise TimeoutError
    
    def submit_otp(self):

        try:

            otp_inputs = self.find_elements(By.CSS_SELECTOR,
                                        'input[placeholder="*"]')
            
            # print(len(otp_inputs))
            # print(otp_inputs)

             # Set the signal handler for SIGALRM (alarm signal)
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(300)

            while True:

                otp = input("Enter OTP: ")
                idx = 0

                signal.alarm(0)

                for otp_input in otp_inputs:
                    otp_input.send_keys(otp[idx])
                    idx = idx + 1

                resend_otp = self.find_element(By.CSS_SELECTOR,
                                            'button[class="resend underline mr-2 disabled:opacity-50"]')

                verify_button = self.find_element(By.CSS_SELECTOR,
                                                'button[class="btn shadow-lg p-2 rounded-full font-bold text-sm uppercase bg-primary text-white w-full h-12"]')

                verify_button.click()

                try:
                    msg = WebDriverWait(self, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="display-error ng-star-inserted"]')))
                    print(msg.text)
                except Exception:
                    break

        except Exception as e:
            print(e)
            raise Exception("OTP niye jhamela hoise")
        
        finally:
            signal.alarm(0)

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
            # print(e)
            raise Exception("Unable to fill co-passenger/s name")

    def extract_information(self):
        try:
            trip_data = self.find_element(By.CSS_SELECTOR,
                                          'div[class="card mt-2 single-trip-card"]'
                                          )

            cities_found = trip_data.find_elements(By.CSS_SELECTOR,
                                                   'span[class="trip-card-city-name ng-star-inserted"]'
                                                   )
            # print(cities_found[0].text)
            const.FROM_FOUND = cities_found[0].text

            # to_found = trip_data.find_element(By.CSS_SELECTOR,
            #                                   'span[class="trip-card-city-name ng-star-inserted"]'
            #                                   )
            # print(cities_found[1].text)
            const.TO_FOUND = cities_found[1].text

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

            # This part doesn't work , supposed to get the fare but always returns 0
            # fare_found = self.find_element(
            #     By.CSS_SELECTOR, 'div[class="semi flex flex-row space-x-1"]')

            # # print(len(fare_found))

            # print(fare_found.text)
            # const.FARE_FOUND = fare_found.text

            print(const.FROM_FOUND + "--->" + const.TO_FOUND + "\n" + const.TRAIN_FOUND + "\n" +
                  const.CLASS_FOUND + "\n" + const.SEATS + "\n")

            # if (int(data[3].text) < const.NO_OF_TICKETS):
            #     raise Exception("seat_error")

        except Exception as e:
            print("Unable to fetch information")
            # if (str(e) == "seat_error"):
            #     time.sleep(const.WAIT)
            #     raise Exception(
            #         "Number of tickets selected is less than desired")
            # print(e)

    def is_click_confirm_available(self):
        try:
            confirm_purchase_btn = self.find_element(By.CSS_SELECTOR,
                                                     'button[class="btn shadow-lg p-2 rounded-full font-bold text-sm uppercase bg-primary text-white w-full h-12"]')

            if  confirm_purchase_btn:
                    return True
            else:
                return False
        
        except Exception as e:                                                                                       
            raise Exception("Confirm purchase button is not enabled")
        

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
            # print(e)
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
            # print(e)

    def select_payment_method(self):
        try:

            payment_method = "dbbl_nexus"

            # print("Select Payment method")
            # print("1. Bkash (doesn't work right now)")
            # print("2. Rocket")
            # print("3. Nagad")
            # print("4. DBBL_Nexus")
            # payment_option = int(input("Type a number : "))

            # if payment_option == 1:
            #     payment_method = "bkash"

            # elif payment_option == 2:
            #     payment_method = "rocket"

            # elif payment_option == 3:
            #     payment_method = "nagad"

            # elif payment_option == 4:
            #     payment_method = "dbbl_nexus"

            print(payment_method)

            time.sleep(const.WAIT)

            if payment_method == "nagad":

                nagad = self.find_element(By.CSS_SELECTOR,
                                          'img[src="assets/images/select-payment/nagad.svg"]'
                                          )
                time.sleep(const.WAIT)
                nagad.click()
                time.sleep(const.WAIT)
                self.nagad_payment()

            elif payment_method == "bkash":
                bkash = self.find_element(By.CSS_SELECTOR,
                                          'img[src="assets/images/select-payment/bkash_bangla.svg"]'
                                          )  # class="image w-16"
                time.sleep(const.WAIT)
                bkash.click()
                time.sleep(const.WAIT)
                self.bkash_payment()

            elif payment_method == "rocket":

                rocket = self.find_element(By.CSS_SELECTOR,
                                           'img[src="assets/images/select-payment/rocket.svg"]'
                                           )
                time.sleep(const.WAIT)
                rocket.click()
                time.sleep(const.WAIT)
                self.rocket_payment()

            else:

                dbbl_nexus = self.find_element(By.CSS_SELECTOR,
                                               'img[src="assets/images/select-payment/nexus-debit.svg"]'
                                               )
                time.sleep(const.WAIT)
                dbbl_nexus.click()
                time.sleep(const.WAIT)
                self.dbbl_nexus_payment()

            time.sleep(const.WAIT)
            # to_payment_btn.click()

        except Exception as e:
            print("Error selecting payment method")
            raise Exception("Error selecting payment method")
            # print(e)

    def dbbl_nexus_payment(self):

        try:

            to_payment_btn = self.find_element(By.CSS_SELECTOR,
                                               'button[class="btn shadow-lg p-2 rounded-full font-bold text-sm uppercase bg-primary w-full h-12 text-white"]'
                                               )
            time.sleep(const.WAIT)
            to_payment_btn.click()

            name = input("Enter cardholder name : ")
            nameForm = self.find_element(By.ID, "cardname")

            nameForm.send_keys(name)

            cardNumber = input("Enter card number : ")

            cardForm = self.find_element(By.ID, "cardnr")

            cardForm.send_keys(cardNumber)

            pin = input("Enter PIN : ")

            pinForm = self.find_element(By.ID, "cvc2")

            pinForm.send_keys(pin)

            submitBtn = self.find_element(By.ID, "paydiv")

            submitBtn.click()

            while True:

                otp = input("Enter OTP : ")

                otpForm = self.find_element(By.ID, "passCode")

                otpForm.send_keys(otp)

                finalBtn = self.find_element(By.CLASS_NAME, "submit")

                finalBtn.click()

                # msg = self.find_element(By.ID, "msg")
                try:
                    msg = WebDriverWait(self, 5).until(
                        EC.presence_of_element_located((By.ID, "msg")))
                    print(msg.text)
                except Exception as e:
                    break
        except Exception as e:
            print("Payment failed")
            raise Exception("Payment failed")

    def bkash_payment(self):
        try:
            to_payment_btn = self.find_element(By.CSS_SELECTOR,
                                               'button[class="btn shadow-lg p-2 rounded-full font-bold text-sm uppercase bg-primary w-full h-12 text-white"]'
                                               )
            time.sleep(const.WAIT)
            to_payment_btn.click()

            time.sleep(20)

            # mobileNumber = input("Enter mobile number : ")
            mobileNumber = "01948626780"

            numberForm = self.find_element(
                By.CSS_SELECTOR, 'input[placeholder="e.g 01XXXXXXXXX"]')

            numberForm.send_keys(mobileNumber)

            numberConfirmBtn = self.find_element(By.ID, "submit_button")

            numberConfirmBtn.click()

        except Exception as e:
            print("Payment failed")
            print(e)

    def rocket_payment(self):

        try:

            to_payment_btn = self.find_element(By.CSS_SELECTOR,
                                               'button[class="btn shadow-lg p-2 rounded-full font-bold text-sm uppercase bg-primary w-full h-12 text-white"]'
                                               )
            time.sleep(const.WAIT)
            to_payment_btn.click()

            mobileNumber = input("Enter mobile number(12 digits) : ")

            cardForm = self.find_element(By.ID, "cardnr")

            cardForm.send_keys(mobileNumber)

            pin = input("Enter PIN : ")

            pinForm = self.find_element(By.ID, "cvc2")

            pinForm.send_keys(pin)

            submitBtn = self.find_element(By.ID, "paydiv")

            submitBtn.click()

            while True:

                otp = input("Enter OTP : ")

                otpForm = self.find_element(By.ID, "passCode")

                otpForm.send_keys(otp)

                finalBtn = self.find_element(By.CLASS_NAME, "submit")

                finalBtn.click()

                # msg = self.find_element(By.ID, "msg")
                try:
                    msg = WebDriverWait(self, 5).until(
                        EC.presence_of_element_located((By.ID, "msg")))
                    print(msg.text)
                except Exception as e:
                    break
        except Exception as e:
            print("Payment failed")

    def nagad_payment(self):
        try:
            to_payment_btn = self.find_element(By.CSS_SELECTOR,
                                               'button[class="btn shadow-lg p-2 rounded-full font-bold text-sm uppercase bg-primary w-full h-12 text-white"]'
                                               )
            time.sleep(const.WAIT)
            to_payment_btn.click()

            time.sleep(20)

            mobileNumber = input("Enter mobile number: ")

            numberBox = self.find_elements(
                By.CSS_SELECTOR, 'input[class="form-control"]')

            for i in range(11):
                numberBox[i].send_keys(mobileNumber[i])

            proceedBtn = self.find_element(
                By.CSS_SELECTOR, 'button[data-trans-key="proceed_btn"]')
            proceedBtn.click()

            otp = input("Enter OTP : ")

            otpForm = self.find_element(
                By.CSS_SELECTOR, 'input[class="form-control text-center"]')

            otpForm.send_keys(otp)

            proceedBtn = self.find_element(
                By.CSS_SELECTOR, 'button[data-trans-key="proceed_btn"]')
            proceedBtn.click()

            pin = input("Enter PIN: ")

            pinBox = self.find_elements(
                By.CSS_SELECTOR, 'input[class="form-control"]')

            for i in range(4):
                pinBox[i].send_keys(pin[i])

            proceedBtn = self.find_element(
                By.CSS_SELECTOR, 'button[data-trans-key="proceed_btn"]')
            proceedBtn.click()

        except Exception as e:
            print("Payment failed")
            print(e)
