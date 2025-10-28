---
layout: post
title: "How to create Shopping Cart APP with rest api"
date: 2025-10-28
tags: [Interview Prep,rest-api,backend development]
---
### Lets add rest API to Shopping cart APP

## Youtube Video explanation
https://youtube.com/shorts/703YIxSo-kA?feature=share

## Code

```python

from flask import Flask, request, jsonify
from model import ShoppingItem

app = Flask(__name__)

shopping_cart = []

def add_to_cart(item):
    shopping_cart.append(item)
    return "Added to cart"


@app.route('/cart', methods=['POST'])
def add_item():
    data = request.json
    item = ShoppingItem(data['name'], data['tag'])
    result = add_to_cart(item)
    return jsonify({"message": result})

@app.route('/cart', methods=['GET'])
def get_cart():
    cart_items = [{'name': item.name, 
                   'category': item.tag} 
                  for item in shopping_cart]
    return jsonify(cart_items)

def remove_from_cart(item_name):
    global shopping_cart
    for i in range(len(shopping_cart)):
        if shopping_cart[i].name == item_name:
            del shopping_cart[i]
            return f"Item {item_name} removed from cart"
    return f"Item {item_name} not found in cart"

@app.route('/cart', methods=['DELETE'])
def remove_item():
    data = request.json
    item_name = data.get('name')
    if not item_name:
        return jsonify(
            {"error": "Item name is required"}), 400
    result = remove_from_cart(item_name)
    return jsonify({"message": result})


if __name__ == '__main__':
    app.run(debug=True)


```
