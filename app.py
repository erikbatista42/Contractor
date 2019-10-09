from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

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
        "title": request.form.get("title"),
        "image": request.form.get("image").split(),
        "price": request.form.get("price").split(),
        "description": request.form.get("description")
    }
    shirt_id = shirts.insert_one(shirt).inserted_id
    return redirect(url_for("shirt_show", shirt_id=shirt_id))

@app.route("/shirts/<shirt_id>")
def shirt_show(shirt_id):
    shirt = shirts.find_one({"_id": ObjectId(shirt_id)})
    return render_template("shirt_show.html", shirt=shirt)

@app.route("/shirts/<shirt_id>/edit")
def shirt_edit(shirt_id):
    # show edit form
    shirt = shirts.find_one({"_id" : ObjectId(shirt_id)})
    return render_template("shirt_edit.html", shirt=shirt)

@app.route("/shirts/<shirt_id>", methods=["POST"])
def shirt_update(shirt_id):
    updated_shirt = {
        "title": request.form.get("title"),
        "image": request.form.get("image").split(),
        "price": request.form.get("price").split(),
        "description": request.form.get("description")
    }
    shirts.update_one({"_id": ObjectId(shirt_id)},{ "$set": updated_shirt})
    return redirect(url_for("shirt_show", shirt_id=shirt_id))

if __name__ == "__main__":
    app.run(debug=True)