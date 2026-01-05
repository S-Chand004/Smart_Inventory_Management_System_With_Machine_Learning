# Smart Inventory Management System with ML

## Project Overview

This project is a **Smart Inventory Management System** that tracks product stock changes over time and uses **Machine Learning** to predict how long the current inventory will last.

The system records every stock increase and decrease, builds historical data, and trains a **Linear Regression model** to estimate daily product consumption. Based on this prediction, it classifies stock status as **SAFE**, **LOW**, or **CRITICAL**, helping businesses make proactive restocking decisions.

This project demonstrates **backend development**, **database design**, **data ingestion**, and **applied machine learning** in a real-world scenario.

---

## Technologies Used

* **Python**
* **Flask**
* **MySQL**
* **Pandas**
* **Scikit-learn**
* **SQL**
* **Git**


## Project Structure

```
Smart Inventory Management With ML/
│
├── app/
│   ├── analytics/
│   │   └── ml/
│   │       ├── train_model.py
│   │       ├── predict.py
│   │       └── models/
│   ├── routes/
│   └── templates/
│
├── scripts/
│   ├── load_kaggle_data.py
│   ├── test_train.py
│   └── test_predict.py
│
├── data/
│   └── retail_store_inventory.csv
│
├── run.py
└── README.md
```

---

## Setup Instructions

### Clone the Repository

```
git clone <your-github-repo-url>
cd Smart-Inventory-Management-With-ML
```


### Create & Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Database Setup (MySQL)

### Create Database

```sql
CREATE DATABASE inventory_db;
USE inventory_db;
```


### Create `products` Table

```sql
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150),
    category VARCHAR(100),
    quantity INT,
    threshold INT,
    external_product_code VARCHAR(50) UNIQUE,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 3️⃣ Create `stock_history` Table

```sql
CREATE TABLE stock_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    change_type ENUM('increase', 'decrease'),
    change_amount INT,
    resulting_quantity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

---

## Loading the Dataset

Place the Kaggle dataset CSV file here:

```
data/retail_store_inventory.csv
```

Then run:

```bash
python scripts/load_kaggle_data.py
```

This will:

* Insert products into the database
* Generate historical stock events
* Populate ML-ready time-series data

---

## Machine Learning Workflow

### Train Model for a Product

Edit `scripts/test_train.py` and set a valid `PRODUCT_ID`, then run:

```bash
python scripts/test_train.py
```

This trains a **Linear Regression model** using recent stock consumption history and saves it to:

```
app/analytics/ml/models/
```

---

### Run Prediction

Edit `scripts/test_predict.py` with the same `PRODUCT_ID`, then run:

```bash
python scripts/test_predict.py
```

Example Output:

```json
{
  "product_id": 9,
  "predicted_daily_consumption": 137.24,
  "current_stock": 183,
  "days_remaining": 1,
  "status": "CRITICAL"
}
```

---

## How to Run the Application (Sequence)

1. Setup database & tables
2. Load Kaggle dataset
3. Train ML model
4. Run prediction
5. (Optional) Integrate predictions into Flask dashboard

---

## Key Features

* Time-series stock tracking
* External dataset integration
* ML-based consumption prediction
* Low-stock classification
* Scalable data ingestion (chunked & batch processing)

---

## Future Enhancements

* Auto-train model on stock update
* Low-stock alerts (email / notifications)
* Product name management UI
* Advanced ML models (moving averages, ARIMA)


