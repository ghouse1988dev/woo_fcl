import pprint
from dotenv import dotenv_values
import requests
import json
import ssl
from pprint import pprint
ssl._create_default_https_context = ssl._create_unverified_context

API_URL = "https://api.hyros.com/v1/api/v1.0/orders"  # Replace with your actual API URL
creds = dotenv_values("creds.env")
headers = {'API-Key': creds['hyro_key']}  # Replace with your actual API key


def create_order(extracted_data,sale_ids):
        
    body = extracted_data
    body = json.dumps(extracted_data)
    """r = requests.post(API_URL, data=body, headers=headers)
    print(r.status_code)
    if r.status_code == 200:
        for sale_id in sale_ids:
            del_sale = requests.delete(f'https://api.hyros.com/v1/api/v1.0/sales/{sale_id}', headers=headers)"""

    pprint(body)
    print(sale_ids)
    print("Order Created")