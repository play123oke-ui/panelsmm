#!/bin/python3                                             psmm.p#!/bin/python3
# Panelsmm
# script_panel.py

import os
import secrets
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///panelsmm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api_key = secrets.api_key
app.config['SECRET_KEY'] = api_key
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Float, default=0.0)

class Deposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    services = Service.query.all()
    return render_template('index.html', services=services)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Masuk ke login")
    if request.method == 'POST':
        print("Masuk ke post login")
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            print("Login berhasil")
            return redirect(url_for('dashboard'))
    print("Login gagal")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    user = User.query.first()
    deposits = Deposit.query.filter_by(user_id=user.id).all()
    orders = Order.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', user=user, deposits=deposits, orders=orders)

@app.route('/services')
def services():
    services = Service.query.all()
    return render_template('services.html', services=services)

@app.route('/add_service', methods=['GET', 'POST'])
def add_service():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        service = Service(name=name, description=description, price=price)
        db.session.add(service)
        db.session.commit()
        return redirect(url_for('services'))
    return render_template('add_service.html')

if __name__ == '__main__':
    print(f"API Key: {api_key}")
    app.run(debug=True, port=5000)
