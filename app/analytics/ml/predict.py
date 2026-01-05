import os
import pickle
import mysql.connector
import pandas as pd

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "s@chand",
    "database": "inventory_db",
}

MODEL_DIR = "app/analytics/ml/models"

def predict_stock_status(product_id):
    """
    Predicts daily consumption and estimates
    how many days stock will last.
    """

    model_path = os.path.join(
        MODEL_DIR, f"product_{product_id}.pkl"
    )

    if not os.path.exists(model_path):
        print(f"No trained model found for product {product_id}")
        return None

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT quantity, threshold
        FROM products
        WHERE id = %s
        """,
        (product_id,),
    )

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        print("Product not found")
        return None

    current_stock, threshold = row

    X_next = pd.DataFrame([[1]], columns=["day_index"])
    predicted_daily_consumption = model.predict(X_next)[0]

    if predicted_daily_consumption <= 0:
        predicted_daily_consumption = 1

    days_remaining = current_stock / predicted_daily_consumption

    if days_remaining <= 3:
        status = "CRITICAL"
    elif days_remaining <= 7:
        status = "LOW"
    else:
        status = "SAFE"

    return {
        "product_id": product_id,
        "predicted_daily_consumption": round(predicted_daily_consumption, 2),
        "current_stock": current_stock,
        "days_remaining": int(days_remaining),
        "status": status,
    }
