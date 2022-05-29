#python 3
import requests, hashlib, time, base64, hmac, pprint

headers1 = {
    'Accept': '*/*'
}
headers2 = {
    'Accept': 'application/json'
}
headers3 = {
  'Content-Type': 'application/json',
  'Accept': '*/*'
}
headers4 = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}


key = ""  #Key
un = ""   #Username
skey = "" #Secret Key

def create_private_data():
    ts = str(int(time.time()))
    message = '{}{}{}'.format(ts,un,key)
    password = hmac.new(bytes(skey, 'latin-1'), msg = bytes(message, 'latin-1'), digestmod = hashlib.sha256).hexdigest().upper()
    private_data = {
        "key": key,
        "signature": password,
        "nonce": ts
    }
    return private_data

# ------ Public API Calls ------

def currency_limits():
    return requests.get("https://cex.io/api/currency_limits", headers = headers2).json()

def ticker(symbol1, symbol2):
    return requests.get(f"https://cex.io/api/ticker/{symbol1}/{symbol2}", headers = headers1).json()

def ticker_by_pair(arr):
    url = "https://cex.io/api/tickers"
    for i in arr:
        url += '/' + i
    return requests.get(url, headers = headers1).json()

def last_price(symbol1, symbol2):
    return requests.get(f"https://cex.io/api/last_price/{symbol1}/{symbol2}", headers = headers1).json()

def last_price_by_pair(arr):
    url = "https://cex.io/api/last_prices"
    for i in arr:
        url += '/' + i
    return requests.get(url, headers = headers1).json()

def convert(symbol1, symbol2, amount):
    data = {
        "amnt": float(amount)
    }
    return requests.post(f"https://cex.io/api/convert/{symbol1}/{symbol2}", headers = headers1, data = data).json()

def chart(symbol1, symbol2, hours, size):
    data = {
        "lastHours": hours,
        "maxRespArrSize": 100
    }
    return requests.post(f"https://cex.io/api/price_stats/{symbol1}/{symbol2}", headers = headers1, data = data).json()

def order_book(symbol1,symbol2):
    return requests.get(f"https://cex.io/api/order_book/{symbol1}/{symbol2}/", headers = headers1).json()

def trade_history(symbol1,symbol2):
    return requests.get(f"https://cex.io/api/trade_history/{symbol1}/{symbol2}/", headers = headers1).json()

def currency_profile():
    return requests.get("https://cex.io/api/currency_profile", headers = headers2).json()

# ------ Private API Calls ------

def balance():  
    private_data = create_private_data()
    return requests.post("https://cex.io/api/balance/", headers = headers1, data = private_data).json()

def open_orders_list():
    private_data = create_private_data()
    return requests.post("https://cex.io/api/open_orders/", headers = headers1, data = private_data).json()

def open_orders_list_by_pair(symbol1, symbol2):
    private_data = create_private_data()
    private_data['symbol1'] = symbol1
    private_data['symbol2'] = symbol2
    return requests.post(f"https://cex.io/api/open_orders/{symbol1}/{symbol2}", headers = headers1, data = private_data).json()

def open_orders_by_symbol(symbol1):
    private_data = create_private_data()
    return requests.post(f"https://cex.io/api/open_orders/{symbol1}", headers = headers1, data = private_data).json()

def mass_cancel_place_orders(cancel_orders,place_orders,cancelPlacedOrdersIfPlaceFailed):
    private_data = create_private_data()
    private_data["cancel-orders"] = cancel_orders
    private_data["place-orders"] = place_orders
    private_data["cancelPlacedOrdersIfPlaceFailed"] = cancelPlacedOrdersIfPlaceFailed
    return requests.post("https://cex.io/api/mass_cancel_place_orders", headers = headers2, data = private_data).json()

def active_order_status(orders_list):
    private_data = create_private_data()
    private_data["orders_list"] = orders_list
    return requests.post("https://cex.io/api/active_orders_status", headers = headers1, data = private_data).json()

def archived_orders(symbol1,symbol2):
    private_data = create_private_data()
    return requests.post(f"https://cex.io/api/archived_orders/{symbol1}/{symbol2}", headers = headers1, data = private_data).json()

def cancel_order(id):
    private_data = create_private_data()
    private_data["id"] = id
    return requests.post("https://cex.io/api/cancel_order/", headers = headers1, data = private_data).json()

def cancel_all_orders_by_pair(symbol1,symbol2):
    private_data = create_private_data()
    return requests.post(f"https://cex.io/api/cancel_orders/{symbol1}/{symbol2}", headers = headers1, data = private_data).json()

def place_order(symbol1,symbol2,amount,price,order_type):
    private_data = create_private_data()
    private_data["order_type"] = "market"
    private_data["type"] = order_type
    private_data["amount"] = float(amount)
    private_data["price"] = float(price)
    return requests.post(f"https://cex.io/api/place_order/{symbol1}/{symbol2}", headers = headers1, data = private_data).json()

def get_order_details(id):
    private_data = create_private_data()
    private_data["id"] = id
    return requests.post("https://cex.io/api/get_order/", headers = headers1, data = private_data).json()

def get_order_transactions(id):
    private_data = create_private_data()
    private_data["id"] = id
    return requests.post("https://cex.io/api/get_order_tx/", headers = headers1, data = private_data).json()

def get_crypto_adress(currency):
    private_data = create_private_data()
    private_data["currency"] = currency
    return requests.post("https://cex.io/api/get_address/", headers = headers1, data = private_data).json()

def get_all_crypto_adresses(currency):
    private_data = create_private_data()
    private_data["currency"] = currency
    return requests.post("https://cex.io/api/get_crypto_address/", headers = headers2, data = private_data).json()

def get_fee():
    private_data = create_private_data()
    return requests.post("https://cex.io/api/get_myfee/", headers = headers1, data = private_data).json()

def cancel_replace_order(symbol1,symbol2,order_type,amount,price,id):
    private_data = create_private_data()
    private_data["type"] = order_type
    private_data["amount"] = amount
    private_data["price"] = price
    private_data["id"] = "\"" + id + "\""
    return requests.post(f"https://cex.io/api/cancel_replace_order/{symbol1}/{symbol2}", headers = headers1, data = private_data).json()

def currency_profile():
    private_data = create_private_data()
    return requests.post("https://cex.io/api/currency_profile", headers = headers2, data = private_data).json()
