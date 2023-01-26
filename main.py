import time
from ticketbooking import constants as const
from datetime import datetime
from ticketbooking.bookticket import Booking

print(const.DATE)
fetchURL = False

while True:
    bot = Booking()
    try:
        # if fetchURL == False:
        #     bot.land_first_page()
        # fetchURL = True
        bot.land_first_page()
        bot.login()
        bot.click_agree_btn()

        # while True:
        #     t = datetime.now()
        #     if t.minute == 53 and t.second == 42:
        #         bot.land_first_page()
        #         break

        bot.fill_stations(const.FROM , const.TO)
        # bot.fill_stations("Dinajpur" , "Dhaka")
        bot.select_date_and_class(const.DATE)
        bot.search_trains()
        booking_page_url = bot.get_url()
        bot.change_wait(10)

        while True:
            try:
                bot.book_now(const.CLASS , const.NO_OF_TICKETS , const.TRAIN)
                # bot.land_booking_page(booking_page_url)
                break
            except Exception as e:
                if str(e) == "No train found by this name":
                    bot.close()
                    break
                print(e)
                bot.land_page(booking_page_url)
        break
    except:
        # bot.__exit__()
        # bot.land_page(const.BASE_URL)
        bot.close()
        # bot.refresh()
        print("Jhamela hoise")
        # if bot.isBrowserAlive() == False:
        #     break
    time.sleep(1)