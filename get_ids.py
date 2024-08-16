from dotenv import dotenv_values
import requests
import ssl
import invoices
from pprint import pprint

ssl._create_default_https_context = ssl._create_unverified_context
creds = dotenv_values("creds.env")
# Configuration
API_URL = "https://api.hyros.com/v1/api/v1.0/sales" 
headers = {'API-Key': creds['hyro_key']}

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

    result_list = []
    request_ids = []
    next_page_ids = []
    grouped_data = {}

    while True:
        data = fetch_data(API_URL, headers, params)
        print(data.keys())
        
        # Extract requestId and nextPageID from the response
        request_id = data['request_id']
        
        # Iterate over each record in the JSON data
        for record in data['result']:
            
            
            email = record['lead'].get('email')
            if email.endswith("paypal.com"):
                orderId = record.get('orderId')
                sale_id = record['id']

        # Create a dictionary with the required information
                extracted_info = {
                    'orderId': orderId,
                    'email': email,
                    'saleId':sale_id
                    }
                result_list.append(extracted_info)
        for item in result_list:
            orderId = item['orderId']
            saleId = item['saleId']

            # If the orderId is not in the dictionary, add it with the email and an empty list for saleIds
            if orderId not in grouped_data:
                grouped_data[orderId] = {
                    'saleIds': []
                }
            grouped_data[orderId]['saleIds'].append(saleId)

        #deduped_list = [i for n, i in enumerate(result_list) if i not in result_list[:n]]
        result = [{'orderId': orderId, 'saleIds': details['saleIds']} for orderId, details in grouped_data.items()]   

            # Append the dictionary to the result list
            

        if request_id:
            request_ids.append(request_id)
            headers['request_id'] = request_id
                
        if 'nextPageId' in data.keys():
            next_page_id = data['nextPageId']
            next_page_ids.append(next_page_id)
            params['pageId'] = next_page_id  # Update the page parameter for the next request
        else:
            break  # Exit loop if  nextPageID is not present

    print("Request IDs:", request_ids)
    print("Next Page IDs:", next_page_ids)
    #print("Order Data:", result)
    
    #return result_list
    invoices.get_invoices(result, fromDate, toDate)