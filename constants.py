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
# CLASSES = ["S_CHAIR", "SNIGDHA", "AC_S", "AC_B", "F_BERTH"]
# TRAINS = ["BANALATA EXPRESS (791)", "SILKCITY EXPRESS (754)",
#           "PADMA EXPRESS (760)", "DHUMKETU EXPRESS (770)" , "EKOTA EXPRESS (705)"]
BLOCKED_CLASSES = [ac_s]
BLOCKED_TRAIN = []
# FROMLIST = ["Natore", "Ishwardi Bypass", "Ullapara", "SH M Monsur Ali"]
# TOLIST = ["Dinajpur", "B Sirajul Islam"]
FROMLIST = ["Rajshahi", "Ishwardi Bypass", "Abdulpur"]
TOLIST = ["Dhaka"]
DATELIST = ["01-Jan-2024"]


# Modify here according to your requirement
FROM = "Ishwardi Bypass"
TO = "Dhaka"
TRAIN = silkcity
TRAINS = ["DHUMKETU EXPRESS (769)", "NILSAGAR EXPRESS (765)",
          "RANGPUR EXPRESS (771)", "EKOTA EXPRESS (705)"]
CLASS = snigdha
NO_OF_TICKETS = 1

# Give the name of co passenger's if two or more ticket needed(Don't Include account holder name)
PASSENGER_NAMES = ["ABCDE", "FGHHIJ", "KLMNO"]
# How many days left to your journey
DAYS_TO_JOURNEY = 3

# An advance option for train and class selecting
# (All these options will first look for preferred train and class , if not found then these options will be useful)
# 1 = Default , if preferred train and class not found then available ticket from any train/class will be booked (suggested)
# 2 = It will book ticket from desired train only
# 3 = It will book ticket of desired class from any of the available train
# 4 = It will only book ticket from desired train and class only (most restrictive option)
# 5 = It will book from the list of the desired trains
BOOK_NOW_OPTION = 2

# Insert your chromedriver path here
DRIVER_PATH = "/usr/local/bin/chromedriver"

# Modify according to your .env file or plainly put value here , e. g MOBILE = "01#########"
MOBILE = os.environ['MY_GP']
PASSWORD = os.environ['MY_GP_PASS']

MOBILE = os.environ['MY_BL']
PASSWORD = os.environ['MY_BL_PASS']

# MOBILE = os.environ['SAKIB_ROBI']
# PASSWORD = os.environ['SAKIB_ROBI_PASS']

# MOBILE = os.environ['MY_ROBI']
# PASSWORD = os.environ['MY_ROBI_PASS']

# MOBILE = os.environ['ABBU_GP']
# PASSWORD = os.environ['ABBU_GP_PASS']

# MOBILE = os.environ['SOUROVE_GP']
# PASSWORD = os.environ['SOUROVE_GP_PASS']

# MOBILE = os.environ['RUPA_GP']
# PASSWORD = os.environ['RUPA_GP_PASS']

# MOBILE = os.environ['MAOI_ROBI']
# PASSWORD = os.environ['MAOI_ROBI_PASS']

# MOBILE = os.environ['NAHID_AIRTEL']
# PASSWORD = os.environ['NAHID_AIRTEL_PASS']

# MOBILE = os.environ['MASUD_BL']
# PASSWORD = os.environ['MASUD_BL_PASS']

# MOBILE = os.environ['MASUD_AIRTEL']
# PASSWORD = os.environ['MASUD_AIRTEL_PASS']

# MOBILE = os.environ['RABBENY_AIRTEL']
# PASSWORD = os.environ['RABBENY_AIRTEL_PASS']

# Modify according to your .env file or plainly put here
SENDER_EMAIL = os.environ['SENDER_EMAIL']
RECEIVER_EMAIL = []
RECEIVER_EMAIL = [os.environ['MY_EMAIL']]
# RECEIVER_EMAIL = [os.environ['MY_EMAIL'], os.environ['KASHEM_EMAIL']]
# RECEIVER_EMAIL = [os.environ['MY_EMAIL'], os.environ['FAHIM_EMAIL']]
# RECEIVER_EMAIL = [os.environ['MY_EMAIL'], os.environ['NAHID_EMAIL']]
# RECEIVER_EMAIL = [os.environ['MY_EMAIL'], os.environ['MASUD_EMAIL']]
# RECEIVER_EMAIL = [os.environ['MY_EMAIL'], os.environ['RABBENY_EMAIL']]
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
