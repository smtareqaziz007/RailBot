#create a file exactly in this format name constants.py
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
f_seat = "F_SEAT"
f_berth = "F_BERTH"
snigdha = "SNIGDHA"
silkcity = "SILKCITY"
banalata = "BANALATA"
dhumketu = "DHUMKETU"
padma = "PADMA"


BLOCKED_CLASSES = ["SHOVAN"]
BLOCKED_TRAIN = []

# If you want search train on multiple days or routes
FROMLIST = [""]
TOLIST = [""]
DATELIST = ["10-Apr-2022"]
GENERATE_URL = 0


# Modify here according to your requirement
FROM = "Dhaka"
TO = "Rajshahi"
TRAIN = "Padma"
TRAINS = [] #It is required only if you choose BOOK_NOW_OPTION = 5
CLASS = s_chair
NO_OF_TICKETS = 1

# Give the name of co passenger's if two or more ticket needed(Don't Include account holder name)
PASSENGER_NAMES = []
# How many days left to your journey (0-10)
DAYS_TO_JOURNEY = 10

# An advance option for train and class selecting
# (All these options will first look for preferred train and class , if not found then these options will be useful)
# 1 = Default , if preferred train and class not found then available ticket from any train/class will be booked (suggested)
# 2 = It will book ticket from desired train only
# 3 = It will book ticket of desired class from any of the available train
# 4 = It will only book ticket from desired train and class only (most restrictive option)
# 5 = It will book from the list of the desired trains
BOOK_NOW_OPTION = 2

# Insert your chromedriver path here or include chromedriver in your PATH variable
DRIVER_PATH = "/usr/local/bin/chromedriver"

# Modify according to your .env file or plainly put value here , e. g MOBILE = "01#########"
MOBILE = os.environ['MOBILE_NUM']
PASSWORD = os.environ['PASSWORD']


# Modify according to your .env file or plainly put here
SENDER_EMAIL = os.environ['SENDER_EMAIL']
RECEIVER_EMAIL = []
RECEIVER_EMAIL = [os.environ['RECEIVER_EMAIL']]

GMAIL_PASS = os.environ['GMAIL_PASS_KEY']

FROM_FOUND = ""
TO_FOUND = ""
FARE_FOUND = ""
TRAIN_FOUND = ""
TRAIN_TIME = ""
CLASS_FOUND = ""
SEATS = ""


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
