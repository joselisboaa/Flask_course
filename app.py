from flask import Flask

app = Flask(__name__)

city = [
    {
        "name": "Fortaleza"
    }
]

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
            }
        ]
    }
]


@app.get("/store")
def get_stores():
    return {"stores": stores}


@app.get("/city")
def get_city():
    return {"city": city}
