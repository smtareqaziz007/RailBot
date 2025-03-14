from user import user_input
import time
import constants as const
from datetime import datetime
from ticketbooking.bookticket import Booking
from notification import notify


# user_input.input_data()
print("From : " + const.FROM)
print("To : " + const.TO)
print("Desired Train : " + const.TRAIN)
print("Desired Trains : " + str(const.TRAINS))
print("Desired Class : " + const.CLASS)
print(const.DATE)
print(const.MOBILE)
print("Blocked Trains : " + str(const.BLOCKED_TRAIN))
print("Blocked Classes : " + str(const.BLOCKED_CLASSES))

while True:
    bot = Booking()
    try:
        bot.land_first_page(const.BASE_URL)
        bot.login(const.MOBILE, const.PASSWORD)

        time.sleep(2)
        current_url = bot.get_url()

        # If got pushed in queue for heavy load
        # while bot.get_url == "https://railapp.railway.gov.bd/splash/throttling":
        #     bot.refresh()
        #     time.sleep(4)
        #     print("Refreshed")

        bot.click_agree_btn()

        bot.fill_stations(const.FROM, const.TO)
        bot.select_date_and_class(const.DATE)
        bot.search_trains()
        booking_page_url = bot.get_url()
        bot.change_wait(3)

        # use this if you want to halt execution until a certain time
        # bot.wait_until_time(minute=59, second=58)

        urls = []
        urls.append(booking_page_url)
        if const.GENERATE_URL:
            urls += bot.generate_urls(booking_page_url)
        # print(urls)
        url_num = len(urls)
        count = 0

        while True:
            try:
                count += 1
                bot.book_now()
                seat_selected = bot.select_seat(
                    const.NO_OF_TICKETS)
                
                bot.extract_information()

                is_button_available = bot.is_click_confirm_available()

                if not is_button_available:
                    raise Exception("No ticket is being selected")
                
                # bot.click_confirm_purchase(seat_selected)

                # uncomment to use notification if you aren't near your pc
                # notify.noise()
                # notify.voice()
                if const.RECEIVER_EMAIL:
                    notify.mail()


                # bot.submit_otp()

                # if (const.NO_OF_TICKETS > 1):
                #     bot.fill_passenger_name(const.PASSENGER_NAMES)

                # bot.click_proceed()

                # bot.select_payment_method()

                break
            except Exception as e:
                # if str(e) == "No train found by this name":
                #     bot.close()
                #     break
                print(e)
                count = count % url_num
                bot.land_page(urls[count])
        break
    except Exception as e:
        bot.close()
        print(e)
        # bot.refresh()
        print("Website took too long to respond.\nReloading...")
        # if bot.isBrowserAlive() == False:
        #     break
    time.sleep(1)
