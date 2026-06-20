import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Метод для добавления CORS-заголовков, чтобы GitHub Pages мог слать запросы
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,X-Admin-Login,X-Admin-Pass')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
    return response

SKINS_FILE = 'skins.json'
ORDERS_FILE = 'orders.json'

def read_json(filename, default_value):
    if not os.path.exists(filename):
        return default_value
    with open(filename, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return default_value

def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# API: Получить скины
@app.route('/api/skins', methods=['GET'])
def get_skins():
    skins = read_json(SKINS_FILE, [])
    return jsonify(skins)

# API: Получить заказы (для админки)
@app.route('/api/orders', methods=['GET', 'OPTIONS'])
def get_orders():
    if request.method == 'OPTIONS':
        return '', 200
        
    login = request.headers.get('X-Admin-Login')
    password = request.headers.get('X-Admin-Pass')
    
    if login == 'ponza23ssd' and password == 'ponzic23ssd':
        orders = read_json(ORDERS_FILE, [])
        return jsonify(orders)
    return jsonify({"error": "Unauthorized"}), 401

# API: Создать новый заказ
@app.route('/api/orders', methods=['POST', 'OPTIONS'])
def create_order():
    if request.method == 'OPTIONS':
        return '', 200
        
    data = request.json
    orders = read_json(ORDERS_FILE, [])
    
    new_order = {
        "id": data.get("id"),
        "user": data.get("user"),
        "skin": data.get("skin"),
        "nick": data.get("nick"),
        "trade": data.get("trade")
    }
    orders.append(new_order)
    write_json(ORDERS_FILE, orders)
    return jsonify({"status": "success"})

# API: Удалить заказ
@app.route('/api/orders/<int:order_id>', methods=['DELETE', 'OPTIONS'])
def delete_order(order_id):
    if request.method == 'OPTIONS':
        return '', 200
        
    login = request.headers.get('X-Admin-Login')
    password = request.headers.get('X-Admin-Pass')
    
    if login == 'ponza23ssd' and password == 'ponzic23ssd':
        orders = read_json(ORDERS_FILE, [])
        orders = [o for o in orders if o['id'] != order_id]
        write_json(ORDERS_FILE, orders)
        return jsonify({"status": "deleted"})
    return jsonify({"error": "Unauthorized"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)