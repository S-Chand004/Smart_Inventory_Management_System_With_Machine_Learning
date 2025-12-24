from flask import Blueprint, render_template, redirect, url_for, request
from app.models.db import mysql

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/products')
def products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, category, quantity, threshold FROM products")
    items = cur.fetchall()
    cur.close()

    return render_template('products.html', items = items)

@inventory_bp.route('/add-product', methods = ['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        quantity = request.form['quantity']
        threshold = request.form['threshold']

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO products (name, category, quantity, threshold) VALUES (%s, %s, %s, %s)", (name, category, quantity, threshold))
        
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('inventory.products'))
    return render_template('add_product.html')
