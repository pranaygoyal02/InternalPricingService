#!flask/bin/python
from flask import Flask,jsonify,abort
from flask import make_response,url_for
from flask import request
import json

app = Flask(__name__)
price_tasks = [
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
    "id":101
}
]

# def make_public_task(task):
#     new_task = {}
#     for field in task:
#         if field == 'id':
#             new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
#         else:
#             new_task[field] = task[field]
#     return new_task
def parse_product_value(product_id):
    # price_list = price_tasks['prices']
    # for item in price_list:
    #     if product_id == item['product_id']:
    #         return item[]
    item = [ item for item in price_tasks['prices'] if item['product_id'] == product_id ]
    return item


def calculate_price(orders):

     for order in orders:
         if "items" in order.keys():
            item_list_on_order = order["items"]
            for productids in item_list_on_order and len(item_list_on_order) !=  0 :
                parse_product_value(productids['product_id'])
            pass

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': orders})


@app.route('/todo/api/v1.0/tasks/<int:order_id>', methods=['GET'])
def get_task(order_id):
    order = [order for order in orders if order['id'] == order_id]
    calculate_price(order)
    if len(order) == 0:
        abort(404)
    return jsonify({'order': order[0]})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': price_tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    price_tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in price_tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in price_tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    price_tasks.remove(task[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)