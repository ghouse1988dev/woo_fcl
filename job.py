from datetime import datetime, timedelta, timezone
import pytz
import get_ids



def fetch_sales_data():
    # Get the current time in UTC
    
    tz = pytz.timezone('America/New_York')
    now = datetime.now(tz)
    
    
    #Calculate fromDate and toDate
    #from_date = now - timedelta(hours=6)
    toDate = now
    fromDate = toDate - timedelta(hours=12)
       
    
    """# Format dates to the required format
    from_date_str = from_date.strftime("%Y-%m-%dT%H:%M:%S")
    to_date_str = to_date.strftime("%Y-%m-%dT%H:%M:%S")
    
    # Set the parameters    
    fromDate = from_date_str
    toDate = to_date_str"""
    print(fromDate)
    
    print(toDate)        
    get_ids.get_sales(fromDate,toDate)

def main():
    fetch_sales_data()

if __name__ == "__main__":
    main()