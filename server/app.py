#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries', methods=['GET'])
def bakeries():
    bakeries = Bakery.query.all()
    bakery_data = [
        {'id': bakery.id, 'name': bakery.name, 'created_at': bakery.created_at, 'updated_at': bakery.updated_at}
        for bakery in bakeries
    ]
    return jsonify(bakery_data)

@app.route('/bakeries/<int:id>', methods=['GET'])
def bakery_by_id(id):
    bakery = db.session.get(Bakery, id)
    bakery_data = {'id': bakery.id, 'name': bakery.name, 'created_at': bakery.created_at, 'updated_at': bakery.updated_at}
    
    return jsonify(bakery_data)

@app.route('/baked_goods/by_price', methods=['GET'])
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_data = [
        {'id': baked_good.id, 'name': baked_good.name, 'price': baked_good.price, 'created_at': baked_good.created_at, 'updated_at': baked_good.updated_at}
        for baked_good in baked_goods
    ]
    return jsonify(baked_goods_data)

@app.route('/baked_goods/most_expensive', methods=['GET'])
def most_expensive_baked_good():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).first()
    baked_goods_data = {'id': baked_goods.id, 'name': baked_goods.name, 'price': baked_goods.price, 'created_at': baked_goods.created_at, 'updated_at': baked_goods.updated_at}
    
    return jsonify(baked_goods_data)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
