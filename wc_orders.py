from woocommerce import API
from dotenv import dotenv_values
import orderplacer
creds = dotenv_values("creds.env")

wcapi = API(
    url="https://firstclasslabs.com",
    consumer_key=creds['consumer_key'],
    consumer_secret=creds['consumer_secret'],
    version="wc/v3"
)


def fcl_orders(invoice_number,orderId,sale_ids):
    inv_id = invoice_number
    orderId = orderId
    sale_ids = sale_ids
    id = inv_id.replace('WC-','')
    #print("OrderId : ", order_id)
    #print("Invoice ID : ",id)
    data = wcapi.get("orders/{id}".format(id=id)).json()

    phone = []
    customer_ip_address = []
    id = orderId
    first_name = data['billing']['first_name']
    last_name = data['billing']['last_name']
    email = data['billing']['email']
    date_created = data['date_created']
    phone .append(data['billing']['phone'])
    customer_ip_address.append(data['customer_ip_address'])




    line_items = []

    extracted_data = {
        'orderId': id,
        'firstName' : first_name, #(billing{})  -> 
        'lastName' : last_name, #(billing{})  ->
        'email': email, #(billing{})  ->  email
        'phoneNumbers' : phone, # list
        'date' : date_created,
        'leadIps' : customer_ip_address,
        }

    for items in data['line_items']:
        #pprint(items)
        item = {
            'name' : items['name'],
            'price' : items['price'],
            'quantity' : items['quantity'],
            'tag' : f'$woo_fcl_{items['name']}'
            }

        line_items.append(item)

    extracted_data['items'] = line_items

    
    orderplacer.create_order(extracted_data,sale_ids)
