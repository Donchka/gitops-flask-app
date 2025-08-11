from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
db_user = os.environ.get("MYSQL_USER", "root")
db_pass = os.environ.get("MYSQL_PASSWORD", "password")
db_host = os.environ.get("MYSQL_HOST", "mysql")
db_name = os.environ.get("MYSQL_DATABASE", "itemsdb")
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:3306/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

@app.route("/", methods=["GET"])
def list_items():
    items = Item.query.all()
    return jsonify([{"id": i.id, "name": i.name} for i in items])

@app.route("/add", methods=["POST"])
def add_item():
    data = request.get_json()
    item = Item(name=data.get("name"))
    db.session.add(item)
    db.session.commit()
    return jsonify({"id": item.id, "name": item.name}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
