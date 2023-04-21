import constants as const
from datetime import timedelta


def input_data():
    const.MOBILE = input("Enter Mobile number: ")
    const.PASSWORD = input("Enter Password: ")

    const.TRAIN = input("Enter Train Name: ")
    const.FROM = input("Enter Origin Station: ")
    const.TO = input("Enter Destination Station: ")
    const.CLASS = input(
        "Enter Desired Class(S_CHAIR , SNIGDHA , AC_S , AC_B, F_BERTH): ")
    const.NO_OF_TICKETS = input("Enter desired number of tickets:(1-4) ")
    const.DAYS_TO_JOURNEY = int(input("How many days till journey?(0-10) "))
    const.expected_date = const.today + timedelta(days=const.DAYS_TO_JOURNEY)
    const.set_date()

    const.BOOK_NOW_OPTION = input("""
    Enter a number between (1-4)\n
    1. Default Option (Suggested)\n
    2. Book ticket from your desired train only.\n
    3. Book ticket from your desired class only.\n
    4. Book ticket from your desired train and class.\n""")
