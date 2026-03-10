import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# extraction_of_csv_file
df = pd.read_csv('Amazon.csv')
print(df.head())
print(df.columns)

# transformation of Amazon sales data
trans_df = df.drop_duplicates().fillna(0)

order_df = trans_df[["OrderID", "OrderDate", "OrderStatus", "CustomerID", "PaymentMethod", "ShippingCost"]].rename(
    columns={"OrderID": "order_id", "OrderDate": "order_date",
             "OrderStatus": "order_status", "CustomerID": "customer_id", "PaymentMethod": "payment_method", "ShippingCost": "shipping_cost"}
)

order_df['order_id'] = order_df['order_id'].str[3:].astype(int)
order_df['customer_id'] = order_df['customer_id'].str[4:].astype(int)

order_items_df = trans_df[["OrderID", "ProductID", "Quantity", "UnitPrice", "Discount", "Tax"]].rename(
    columns={"OrderID": "order_id", "ProductID": "product_id", "Quantity": "quantity",
             "UnitPrice": "unit_price", "Discount": "discount", "Tax": "tax"
             }
)

order_items_df['order_id'] = order_items_df['order_id'].str[3:].astype(int)
order_items_df['product_id'] = order_items_df['product_id'].str[1:].astype(int)

customer_df = trans_df[["CustomerID", "CustomerName", "City", "State", "Country"]].rename(
    columns={"CustomerID": "customer_id",
             "CustomerName": "customer_name", "City": "city", "State": "state", "Country": "country"}
)

customer_df['customer_id'] = customer_df['customer_id'].str[4:].astype(int)

product_df = trans_df[["ProductID", "ProductName", "Category", "Brand"]].rename(
    columns={"ProductID": "product_id",
             "ProductName": "product_name", "Category": "category", "Brand": "brand"}
)

product_df['product_id'] = product_df['product_id'].str[1:].astype(int)

print(order_df)
print(order_items_df)
print(customer_df)
print(product_df)

# loading the data to the Postgres
user = os.getenv('db_user')
password = os.getenv('db_pass')
db = os.getenv('db_name')
port = os.getenv('db_port')
host = os.getenv('db_host')

url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(url)


customer_df = customer_df.drop_duplicates(subset=['customer_id']).copy()
product_df = product_df.drop_duplicates(subset=['product_id']).copy()

customer_df.to_sql("customers", engine, if_exists="append", index=False)
product_df.to_sql("products", engine, if_exists="append", index=False)
order_df.to_sql("orders", engine, if_exists="append", index=False)
order_items_df.to_sql("order_items", engine, if_exists="append", index=False)
