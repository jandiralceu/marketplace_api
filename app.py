from flask import Flask, request
from flask_smorest import abort

stores = [
    { 
     "name": "My First Store",
     "items": [
         { "name": "Chair", "price": 19.99 }
     ]
     },
]

app = Flask(__name__)

@app.get("/stores")
def get_stores():
    return { "stores": stores }

@app.post("/stores")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    
    return new_store, 201

@app.post("/stores/<string:name>/item")
def create_item(name):
    pass
