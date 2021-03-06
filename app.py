from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

app.secret_key = 'secret_key'

app.config['MONGO_DBNAME'] = 'acme'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/acme'

mongo = PyMongo(app)

# Create Product
@app.route('/product', methods=['POST'])
def create_product():
  _product = request.json
  _name = _product['name']
  _desc = _product['desc']
  _price = _product['price']
  _quantity = _product['qty']

  # if _name and _description and _price and _quantity:
  product_id = mongo.db.products.insert({'name': _name, 'desc': _desc, 'price': _price, 'qty': _quantity})
  new_product = mongo.db.products.find_one({'_id': product_id})
  output = dumps(new_product)
  return output

# Returns all Products
@app.route('/product', methods=['GET'])
def get_products():
  products = mongo.db.products.find({})
  resp = dumps(products)
  return resp

# Return one Product
@app.route('/product/<id>', methods = ['GET'])
def get_product(id):
  product = mongo.db.products.find_one_or_404({'_id': ObjectId(id)})
  return dumps(product)

# Update a product
@app.route('/product/<id>', methods = ['PUT'])
def update_product(id):
  _req = request.json
  _name = _req['name']
  _desc = _req['desc']
  _price = _req['price']
  _qty = _req['qty']
  product = mongo.db.products.find_one_or_404({'_id':ObjectId(id)})
  if product:
    mongo.db.products.update_one({'_id': ObjectId(id)}, {'$set': {'name': _name, 'desc': _desc, 'price': _price, 'qty': _qty}})
    return get_product(id)
  else:
    not_found()

# Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
  product = mongo.db.products.find_one_or_404({'_id':ObjectId(id)})
  if product:
    mongo.db.products.delete_one({'_id':ObjectId(id)})
    return jsonify('Deleted successfully')
  else:
    not_found()

@app.errorhandler(404)
def not_found(error = None):
  message = {'message': 'Not Found '+ request.url, 'status':404}
  resp = jsonify(message)
  resp.status_code = 404
  return resp

if __name__ == '__main__':
  app.run(debug=True)