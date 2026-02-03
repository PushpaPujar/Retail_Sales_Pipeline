import pandas as pd
import sqlite3

print("ETL Process Started")

# =========================
# CONFIG
# =========================
CSV_PATH = r"C:\Users\HP\OneDrive\Desktop\Superstore_sale_data\train.csv"
DB_PATH = r"C:\Users\HP\OneDrive\Desktop\Superstore_sale_data\sales.db"
TABLE_NAME = "sales_data"

# =========================
# EXTRACT
# =========================
df = pd.read_csv(CSV_PATH)
rows_before = len(df)

print(f"Rows extracted: {rows_before}")

# =========================
# TRANSFORM
# =========================

# Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Convert date columns
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")

# Convert numeric column
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

# =========================
# DATA QUALITY CHECK
# =========================
print("Null values:")
print(df[["order_date", "ship_date", "sales"]].isnull().sum())

# =========================
# LOAD (SQLite)
# =========================
conn = sqlite3.connect(DB_PATH)

df.to_sql(
    name=TABLE_NAME,
    con=conn,
    if_exists="replace",   # use "append" for incremental load
    index=False
)

conn.close()

print("ETL Completed Successfully")
print(f"Data loaded into SQLite DB: {DB_PATH}")
print(f"Table name: {TABLE_NAME}")
