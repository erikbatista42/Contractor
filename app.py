from flask import Flask, render_template
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient()
db = client.Store
shirts = db.shirts

# items = [
#     { 'title': 'Cat Videos', 'description': 'Cats acting weird' },
#     { 'title': '80\'s Music', 'description': 'Don\'t stop believing!' }
# ]


@app.route("/")
def index():
    return render_template('home.html', shirts=shirts.find())

if __name__ == "__main__":
    app.run(debug=True)