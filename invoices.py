from datetime import datetime, timedelta
from dotenv import dotenv_values
import requests
import json
import wc_orders
import ssl

# Disable SSL verification (use with caution, not recommended for production)
ssl._create_default_https_context = ssl._create_unverified_context

# Function to write mised Transactions rom Paypal to a file
file_name = 'missing_ids.txt'
def append_line_to_file(file_name, text):
    with open(file_name, 'a') as file:  # 'a' mode opens the file for appending
        file.writelines(text + '\n')


# PayPal API endpoint for obtaining an OAuth 2.0 token
url = 'https://api-m.paypal.com/v1/oauth2/token'
data = {'grant_type': 'client_credentials'}

# Load credentials from .env file
creds = dotenv_values("creds.env")
username = creds['paypal_user']
password = creds['paypal_pwd']

# Function to get invoices for given order IDs within a date range
def get_invoices(order_sales_dict, fromDate, toDate):
    from_date = fromDate #- timedelta(days=1)
    from_date_str = from_date.strftime("%Y-%m-%dT%H:%M:%S")
    to_date_str = toDate.strftime("%Y-%m-%dT%H:%M:%S")

    params = {
        'start_date': from_date_str + '-0400',
        'end_date': to_date_str + '-0400',
        'fields': 'all'
    }

    print("Invoices start date:", params['start_date'])
    print("Invoices end date:", params['end_date'])

    # Request access token
    response = requests.post(url, data=data, auth=(username, password))
    if response.status_code == 200:
        accesstoken = json.loads(response.text)['access_token']
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {accesstoken}'}
        #print("Access token obtained:", accesstoken)
    else:
        print("Failed to obtain access token. Status code:", response.status_code)
        print("Response:", response.text)
        return

    # Process each order ID
    for item in order_sales_dict:
        sale_ids = item['sale_id']
        orderId = item['orderId']
        print("Processing order ID:", orderId)
        params['transaction_id'] = orderId
        
        tx = requests.get('https://api-m.paypal.com/v1/reporting/transactions', headers=headers, params=params)
        
        if tx.status_code != 200:
            print(f"Failed to fetch transaction for order ID {orderId}. Status code:", tx.status_code)
            print("Response:", tx.text)
            continue

        txs = tx.json()
        #print(json.dumps(txs, indent=2))  # Debug: print the full response

        try:
            if 'transaction_details' in txs and len(txs['transaction_details']) > 0:
                transaction_info = txs['transaction_details'][0]['transaction_info']
                if 'invoice_id' in transaction_info:
                    invoice_id = transaction_info['invoice_id']
                    wc_orders.fcl_orders(invoice_id, orderId, sale_ids)
                    print("Order ID:", orderId)
                    print("Invoice ID:", invoice_id)
                else:
                    print(f"No 'invoice_id' found for order ID {orderId}.")
                    text = f"No invoice_id found for order ID: {orderId}. {from_date_str} to {to_date_str}"
                    append_line_to_file(file_name, text)

            else:
                print(f"No transaction details found for order ID {orderId}.")
                text = f"No transaction details found for order ID: {orderId}. {from_date_str} to {to_date_str}"
                append_line_to_file(file_name, text)

                    

        except KeyError as e:
            print(f"KeyError: {e} for order ID {orderId}")


def append_line_to_file(file_name, text):
    with open(file_name, 'a') as file:  # 'a' mode opens the file for appending
        file.writelines(text + '\n')

