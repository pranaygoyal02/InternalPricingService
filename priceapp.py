#!flask/bin/python
from flask import Flask,jsonify,abort
from flask import make_response
from flask import request
import requests
from requests.exceptions import ProxyError
from werkzeug.contrib.cache import SimpleCache


app = Flask(__name__)
product_price_lookup = [
    {
        "prices": [
            {
                "product_id": 1,
                "price": 599,
                "vat_band": "standard"
            },
            {
                "product_id": 2,
                "price": 250,
                "vat_band": "zero"
            },
            {
                "product_id": 3,
                "price": 250,
                "vat_band": "zero"
            },
            {
                "product_id": 4,
                "price": 1000,
                "vat_band": "zero"
            },
            {
                "product_id": 5,
                "price": 1250,
                "vat_band": "standard"
            }
        ],
        "vat_bands": {
            "standard": 0.2,
            "zero": 0
        }
    }
]
orders = [{
    "id": 12345,
    "customer": {},
    "items": [
        {
            "product_id": 1,
            "quantity": 1
        },
        {
            "product_id": 2,
            "quantity": 5
        },
        {
            "product_id": 3,
            "quantity": 1
        }
    ]
},{
    "id": 1000,
    "customer": {},
    "items": [
        {
            "product_id": 3,
            "quantity": 4
        },
        {
            "product_id": 2,
            "quantity": 5
        }
    ]
},{
    "id": 5000,
    "customer": {},
    "items": [
        {
            "product_id": 1,
            "quantity": 8
        },
        {
            "product_id": 3,
            "quantity": 1
        }
    ]
}
]

# The function returns  the price of each product from product_pricing_lookup
def get_product_price(product_id):
    price_lookup = [prod for prod in product_price_lookup[0]['prices'] if product_id == prod['product_id']]
    return price_lookup

# The function returns  the vat bands from product_pricing_lookup
def get_vat_price():
    vat_lookup =  product_price_lookup[0]['vat_bands']
    return vat_lookup


def get_currency_converter_value(val):
    try:
        #Initialize a cache object for each Thread
        cache = SimpleCache(default_timeout=60)
        #This is purely  hack for setting GBP to EUR value to 1.2 to illustrate cache works for the purpose of demo
        cache.set('GBP_EUR',1.12)
        cache.set('GBP_USD',1.36)

        #Check if the value already exist in the currency
        currency_val = cache.get(val)
        if currency_val is None:
            payload = {'q':val,'compact':'ultra','apiKey':'3dddc18b3b03275e8621'}
            r = requests.get('https://free.currconv.com/api/v7/convert',params=payload)
            r_dict = r.json()
            #set the cache for the given currency with default_timeout 300
            for k,v in r_dict():
                cache.set(k,v, timeout=5 * 60)
            return jsonify(r.json())
        else:
            #return the value received
            return jsonify({val:currency_val})
    except ProxyError:
        print("Proxy Error")
        #setting a default value
        return jsonify({val:1.265471})

def calculate_order_price(orders):
     for order in orders:
         if "items" in order.keys():
            item_list_on_order = order["items"]
            particulars =[]
            for productids in item_list_on_order:
                single_product_price_look_up = get_product_price(productids['product_id'])
                vat_look_up = get_vat_price()
                cal_each_product_total = round(productids['quantity'] * single_product_price_look_up[0]['price'],2)
                cal_each_product_vat_total = round(vat_look_up[single_product_price_look_up[0]['vat_band']] * cal_each_product_total,2)
                particulars.append({ "product_id": productids['product_id'],"total_price_per_product": cal_each_product_total,"vat_total":cal_each_product_vat_total})
            return particulars

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': orders})


@app.route('/todo/api/v1.0/tasks/<int:order_id>', methods=['GET'])
def get_task(order_id, total_price=0, total_vat=0):
    order = [order for order in orders if order['id'] == order_id]
    detailed_order_and_price = calculate_order_price(order)
    for x in detailed_order_and_price:
        total_price += x['total_price_per_product']
        total_vat += x['vat_total']
    total_price_with_vat = total_price + total_vat
    final_json = {
        'Total_Price': round(total_price_with_vat,2),
        'Total_vat':total_vat,
        'particulars':detailed_order_and_price,
        'currency':'GBP'
    }

    if len(order) == 0:
        abort(404)
    return jsonify({'order': final_json})

@app.route('/todo/api/v1.0/tasks/<int:order_id>/<curr>', methods=['GET'])
def get_task_currency(order_id,curr,total_price=0, total_vat=0,):
    val = get_currency_converter_value(curr)
    val = val.json[curr]
    order = [order for order in orders if order['id'] == order_id]
    detailed_order_and_price = calculate_order_price(order)
    for x in detailed_order_and_price:
        total_price += x['total_price_per_product']
        total_vat += x['vat_total']
    total_price_with_vat = (total_price + total_vat) * val
    final_json = {
        'Total_Price': round(total_price_with_vat,2),
        'Total_vat':total_vat,
        'particulars':detailed_order_and_price,
        'currency': curr[-3:]
    }

    if len(order) == 0:
        abort(404)
    return jsonify({'order': final_json})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': orders[-1]['id'] + 1,
        'customer': request.json['customer',""],
        'items': request.json.get('items', ""),
    }
    orders.append(task)
    return jsonify({'task': task}), 201

if __name__ == '__main__':
    app.run(debug=True)