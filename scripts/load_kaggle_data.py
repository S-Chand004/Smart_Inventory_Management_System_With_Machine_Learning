import pandas as pd
import mysql.connector


CSV_PATH = "data/retail_store_inventory.csv"
CHUNK_SIZE = 10000
DEFAULT_THRESHOLD = 10


conn = mysql.connector.connect(
    host = "localhost",
    user =  "root",
    password = "s@chand",
    database = "inventory_db")
cur = conn.cursor()

print("Connected to database")


print("Starting Kaggle data load...")

for chunk in pd.read_csv(CSV_PATH, chunksize=CHUNK_SIZE):

    chunk = chunk[
        [
            "Date",
            "Product ID",
            "Category",
            "Inventory Level",
            "Units Sold",
            "Units Ordered",
        ]
    ]

   
    chunk["Date"] = pd.to_datetime(chunk["Date"], errors="coerce")
    chunk = chunk.dropna(subset=["Date"])


    product_rows = []

    for product_code, group in chunk.groupby("Product ID"):
        first_row = group.iloc[0]

        product_rows.append(
            (
                f"Product-{product_code}",          # name
                str(first_row["Category"]),          # category
                int(first_row["Inventory Level"]),   # quantity
                DEFAULT_THRESHOLD,                   # threshold
                str(product_code),                   # external_product_code
            )
        )

    cur.executemany(
        """
        INSERT IGNORE INTO products
        (name, category, quantity, threshold, external_product_code)
        VALUES (%s, %s, %s, %s, %s)
        """,
        product_rows,
    )
    conn.commit()


    cur.execute(
        "SELECT id, external_product_code FROM products"
    )
    product_id_map = {
        row[1]: row[0] for row in cur.fetchall()
    }


    stock_rows = []

    for _, row in chunk.iterrows():
        product_code = row["Product ID"]
        product_id = product_id_map.get(product_code)

        if not product_id:
            continue

        event_date = row["Date"].to_pydatetime()
        resulting_qty = int(row["Inventory Level"])

        units_sold = int(row["Units Sold"])
        units_ordered = int(row["Units Ordered"])

        if units_sold > 0:
            stock_rows.append(
                (
                    product_id,
                    "decrease",
                    units_sold,
                    resulting_qty,
                    event_date,
                )
            )

        if units_ordered > 0:
            stock_rows.append(
                (
                    product_id,
                    "increase",
                    units_ordered,
                    resulting_qty,
                    event_date,
                )
            )

    if stock_rows:
        cur.executemany(
            """
            INSERT INTO stock_history
            (product_id, change_type, change_amount, resulting_quantity, created_at)
            VALUES (%s, %s, %s, %s, %s)
            """,
            stock_rows,
        )
        conn.commit()

print("Kaggle data loaded successfully")

cur.close()
conn.close()
