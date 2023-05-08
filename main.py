from user import user_input
import time
import constants as const
from datetime import datetime
from ticketbooking.bookticket import Booking
from notification import notify


# user_input.input_data()
print(const.DATE)
print(const.MOBILE)

while True:
    bot = Booking()
    try:
        bot.land_first_page(const.BASE_URL)
        bot.login(const.MOBILE, const.PASSWORD)

        time.sleep(2)
        current_url = bot.get_url()
        # print(current_url)

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
        bot.change_wait(9)

        # use this if you want to halt execution until a certain time
        # bot.wait_until_time(minute=59, second=59)

        while True:
            try:
                bot.book_now(const.CLASS, const.NO_OF_TICKETS,
                             const.TRAIN, const.BOOK_NOW_OPTION)
                seat_selected = bot.select_seat(
                    const.NO_OF_TICKETS)
                bot.click_confirm_purchase(seat_selected)
                bot.extract_information()
                # if (const.NO_OF_TICKETS > 1):
                #     bot.fill_passenger_name(const.PASSENGER_NAMES)

                # bot.click_proceed()

                # write "nagad" , "bkash" or "rocket" to payment_method as per your convenience
                # bot.select_payment_method(payment_method="dbbl_nexus")

                # uncomment to use notification if you aren't near your pc
                notify.mail()
                notify.voice()
                # notify.noise()
                break
            except Exception as e:
                if str(e) == "No train found by this name":
                    bot.close()
                    break
                print(e)
                bot.land_page(booking_page_url)
        break
    except:
        bot.close()
        # bot.refresh()
        print("Website took too long to respond.\nReloading...")
        # if bot.isBrowserAlive() == False:
        #     break
    time.sleep(1)
