from dotenv import dotenv_values
import requests
import ssl
import invoices
from pprint import pprint
from collections import defaultdict

ssl._create_default_https_context = ssl._create_unverified_context

creds = dotenv_values("creds.env")

# Configuration
API_URL = "https://api.hyros.com/v1/api/v1.0/sales"  # Replace with your actual API URL
headers = {'API-Key': creds['hyro_key']}  # Replace with your actual API key

def fetch_data(url, headers, params):
    """Fetch data from the API with given URL, headers, and parameters."""
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def get_sales(fromDate,toDate):
    
    from_date_str = fromDate.strftime("%Y-%m-%dT%H:%M:%S")
    to_date_str = toDate.strftime("%Y-%m-%dT%H:%M:%S")
    
    params = {
        # Starting page or initial parameters if needed
        'fromDate':from_date_str+'-04:00',
        'toDate':to_date_str+'-04:00',
        'pageSize':250

    }

    print("Hyro fromDate",params['fromDate'])
    print("Hyro toDate",params['toDate'])

    res_list = []
    request_ids = []
    next_page_ids = []

    while True:
        data = fetch_data(API_URL, headers, params)

                        
        # Extract requestId and nextPageID from the response
        request_id = data['request_id']
        order_sales = defaultdict(list)
        
        # Iterate over each record in the JSON data
        for sale in data['result']:
            order_id = sale['orderId']
            sale_id = sale['id']
            email = sale['lead'].get('email')
            if email.endswith('paypal.com'):
                #print("Email:",email)
                order_sales[order_id].append(sale_id)
                
        #print(order_sales.keys())
        order_sales_dict = [{'orderId': order_id, 'sale_id': sale_ids} for order_id, sale_ids in order_sales.items()]
        #pprint(order_sales_dict)
        
        if request_id:
            request_ids.append(request_id)
            headers['request_id'] = request_id
                
        if 'nextPageId' in data.keys():
            next_page_id = data['nextPageId']
            next_page_ids.append(next_page_id)
            params['pageId'] = next_page_id  # Update the page parameter for the next request
        else:
            break  # Exit loop if  nextPageID is not present

    
    print(order_sales_dict)
    invoices.get_invoices(order_sales_dict, fromDate, toDate)