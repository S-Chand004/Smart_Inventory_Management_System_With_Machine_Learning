import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from app.analytics.ml.train_model import train_model

PRODUCT_ID = 11   # change this

train_model(PRODUCT_ID)
