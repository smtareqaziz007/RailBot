from datetime import datetime, timedelta

BASE_URL = "https://railapp.railway.gov.bd/"
WAIT = 0.4
TIMEOUT = 5

FROM = "Dinajpur"
TO = "Dhaka"
TRAIN = "EKOTA"
CLASS = "SNIGDHA"
NO_OF_TICKETS = 4

ac_b = "AC_B"
ac_s = "AC_S"
s_chair = "S_CHAIR"
snigdha = "SNIGDHA"
silkcity = "SILKCITY"
banalata = "BANALATA"
dhumketu = "DHUMKETU"
padma = "PADMA"
# DATE = "October 24, 2022"


MOBILE = ""
PASSWORD = ""

today = datetime.today()
expected_date = today + timedelta(days=4)
DATE = ""

if expected_date.month == 1:
    DATE += "January"
elif expected_date.month == 2:
    DATE += "February"
elif expected_date.month == 3:
    DATE += "March"
elif expected_date.month == 4:
    DATE += "April"
elif expected_date.month == 5:
    DATE += "May"
elif expected_date.month == 6:
    DATE += "June"
elif expected_date.month == 7:
    DATE += "July"
elif expected_date.month == 8:
    DATE += "August"
elif expected_date.month == 9:
    DATE += "September"
elif expected_date.month == 10:
    DATE += "October"
elif expected_date.month == 11:
    DATE += "November"
elif expected_date.month == 1:
    DATE += "December"

DATE += f" {expected_date.day}, {expected_date.year}"
