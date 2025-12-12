from datetime import datetime

def convert_date(date_input):
    d = datetime.strptime(date_input, "%d-%m-%Y")
    return d.strftime("%Y-%m-%d")
