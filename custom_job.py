from datetime import datetime, timedelta
import pytz
import get_ids

def main():
    tz = pytz.timezone('America/New_York')
    now = datetime.now(tz)
    fromDate = datetime(2024,6,28,00,00,00)
    toDate = datetime(2024,6,30,00,00,00)
    get_ids.get_sales(fromDate,toDate)
    print(fromDate)
    print(toDate)

if __name__ == "__main__":
    main()
