import os
import pickle
import mysql.connector
import pandas as pd
from sklearn.linear_model import LinearRegression


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "inventory_db",
}

MODEL_DIR = "app/analytics/ml/models"
WINDOW_SIZE = 60   

os.makedirs(MODEL_DIR, exist_ok=True)


def train_model(product_id):
    """
    Trains a Linear Regression model for a single product
    using recent consumption history.
    """

    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT created_at, change_amount
        FROM stock_history
        WHERE product_id = %s
        AND change_type = 'decrease'
        ORDER BY created_at DESC
        LIMIT %s
        """,
        (product_id, WINDOW_SIZE),
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    if len(rows) < 5:
        print(f"Not enough data to train model for product {product_id}")
        return None

    df = pd.DataFrame(rows, columns=["date", "consumption"])
    df = df.sort_values("date") 
    df.reset_index(drop=True, inplace=True)

    df["day_index"] = range(len(df))

    X = df[["day_index"]]
    y = df["consumption"]

    model = LinearRegression()
    model.fit(X, y)

    model_path = os.path.join(
        MODEL_DIR, f"product_{product_id}.pkl"
    )

    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print(f"Model trained and saved for product {product_id}")

    return model

