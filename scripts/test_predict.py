import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from app.analytics.ml.predict import predict_stock_status

PRODUCT_ID = 11

result = predict_stock_status(PRODUCT_ID)
print(result)
