import datetime

def main():
    global current_date
    current_date = datetime.date.today().strftime("%d-%m-%Y")
    return

if(__name__ == "__main__"):
    main()
    