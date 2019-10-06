from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient()
db = client.Store
shirts = db.shirts

@app.route("/")
def index():
    return render_template('home.html', shirts=shirts.find())

@app.route("/shirts/new")
def shirts_new():
    # create new shirt to sell
    return render_template("shirts_new.html")

@app.route('/shirts', methods=['POST'])
def shirt_upload():
    # upload new shirt
    shirt = {
        'title': request.form.get('title'),
        'image': request.form.get('image').split(),
        'price': request.form.get('price').split(),
        'description': request.form.get('description')
    }
    shirts.insert_one(shirt)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)