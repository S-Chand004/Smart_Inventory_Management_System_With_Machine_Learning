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

@inventory_bp.route('/update-stock/<int:product_id>', methods = ['GET', 'POST'])
def update_stock(product_id):
    cur = mysql.connection.cursor()

    cur.execute("SELECT name, quantity FROM products WHERE id = %s", (product_id,))

    product = cur.fetchone()

    if not product:
        cur.close()
        return 'Product not found.'

    if request.method == 'POST':
        change_type = request.form['type']
        amount = int(request.form['amount'])

        net_quantity = product[1]

        if change_type == 'increase':
            net_quantity += amount
        else:
            net_quantity -= amount
            if net_quantity < 0:
                net_quantity = 0
        
        cur.execute("UPDATE products SET quantity=%s WHERE id = %s", (net_quantity, product_id))

        cur.execute("INSERT INTO stock_history (product_id, change_type, change_amount, resulting_quantity) VALUES (%s, %s, %s, %s)", (product_id, change_type, amount, net_quantity))

        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('inventory.products'))
    
    cur.close()

    return render_template('update_stock.html', product=product, product_id = product_id)
