from datetime import datetime, timedelta
import dotenv
import os

dotenv.load_dotenv('.env')

BASE_URL = "https://railapp.railway.gov.bd/"
WAIT = 0.4
TIMEOUT = 5

ac_b = "AC_B"
ac_s = "AC_S"
s_chair = "S_CHAIR"
snigdha = "SNIGDHA"
silkcity = "SILKCITY"
banalata = "BANALATA"
dhumketu = "DHUMKETU"
padma = "PADMA"
CLASSES = ["S_CHAIR", "SNIGDHA", "AC_S", "AC_B", "F_BERTH"]


# Modify here according to your requirement
FROM = "Ishwardi Bypass"
TO = "Dhaka"
TRAIN = "Silkcity"
CLASS = snigdha
NO_OF_TICKETS = 1

# Give the name of co passenger's if two or more ticket needed(Don't Include account holder name)
PASSENGER_NAMES = ["ABCDE", "FGHHIJ", "KLMNO"]
# How many days left to your journey
DAYS_TO_JOURNEY = 10

# An advance option for train and class selecting
# (All these options will first look for preferred train and class , if not found then these options will be useful)
# 1 = Default , if preferred train and class not found then available ticket from any train/class will be booked (suggested)
# 2 = It will book ticket from desired train only
# 3 = It will book ticket of desired class from any of the available train
# 4 = It will only book ticket from desired train and class only (most restrictive option)
BOOK_NOW_OPTION = 4

# Insert your chromedriver path here
DRIVER_PATH = "/usr/local/bin/chromedriver"

# Modify according to your .env file or plainly put here
# MOBILE = os.environ['MY_GP']
# PASSWORD = os.environ['MY_GP_PASS']

MOBILE = os.environ['MY_BL']
PASSWORD = os.environ['MY_BL_PASS']


# Modify according to your .env file or plainly put here
SENDER_EMAIL = os.environ['SENDER_EMAIL']
RECEIVER_EMAIL = os.environ['MY_EMAIL']
GMAIL_PASS = os.environ['GMAIL_PASS_KEY']


today = datetime.today()
DATE = ""
Months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

expected_date = today + timedelta(days=DAYS_TO_JOURNEY)
DATE += Months[expected_date.month - 1]
DATE += f" {expected_date.day}, {expected_date.year}"


def set_date():
    global DATE
    DATE = ""
    DATE += Months[expected_date.month - 1]
    DATE += f" {expected_date.day}, {expected_date.year}"
