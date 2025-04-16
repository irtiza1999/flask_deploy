#Install the required Python packages
# pip install flask
# pip install flask_sqlalchemy
# pip install sqlalchemy


from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os

app = Flask(__name__)

# Database Configuration
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "ecommerce_secret"


db = SQLAlchemy(app)

# ------------ Product Model ------------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=False)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     address = db.Column(db.String(500), nullable=False)

# Create Database Tables
with app.app_context():
    db.create_all()

# ------------ Routes ------------

# Home Route (Displays Products)
@app.route("/")
def home():
    products = Product.query.all()
    return render_template("home.html", products=products)

# Create a Product (POST)
@app.route("/add_product", methods=["POST"])
def add_product():
    name = request.form.get("name")
    price = request.form.get("price")
    description = request.form.get("description")
    
    new_product = Product(name=name, price=price, description=description)
    db.session.add(new_product)
    db.session.commit()
    
    return redirect("/")

# Read Products (GET)
@app.route("/get_products", methods=["GET"])
def get_products():
    products = db.session.execute(text("SELECT * FROM Product")).fetchall()
    return jsonify([dict(row._mapping) for row in products])

# Update a Product (PUT)
@app.route("/update_product/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get(product_id)
    if product:
        product.name = request.form.get("name", product.name)
        product.price = request.form.get("price", product.price)
        product.description = request.form.get("description", product.description)
        
        db.session.commit()
        return redirect("/")
    return "Product Not Found", 404

# Delete a Product (DELETE)
@app.route("/delete_product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return redirect("/")
    return "Product Not Found", 404

# Run the App
if __name__ == "__main__":
    app.run(debug=True)
