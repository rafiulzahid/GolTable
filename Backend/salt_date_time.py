from datetime import datetime
import string, random


# return 36 characters based text
def get_salt():
    random_text = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    current_time = str(datetime.now())

    return (random_text + current_time)

def get_date():
    current_date = datetime.now().date()
    return current_date

def get_time():
    current_time = datetime.now().time().replace(microsecond=0)
    return current_time
