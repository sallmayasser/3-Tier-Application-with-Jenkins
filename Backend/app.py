import os
import pandas as pd
import psycopg2
import time

# DB connection using Jenkins credentials

for i in range(10):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            database=os.getenv("DB_NAME", "customers"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        break
    except psycopg2.OperationalError:
        print("DB not ready, retrying...")
        time.sleep(10)
else:
    raise Exception("Database not available")


# Load CSV
df = pd.read_csv("customers.csv")

# Rename columns
df = df.rename(columns={
    "Index": "idx",
    "Customer Id": "customer_id",
    "First Name": "first_name",
    "Last Name": "last_name",
    "Company": "company",
    "City": "city",
    "Country": "country",
    "Phone 1": "phone1",
    "Phone 2": "phone2",
    "Email": "email",
    "Subscription Date": "subscription_date",
    "Website": "website"
})

# Merge First + Last Name → Full Name
df["full_name"] = df["first_name"].fillna(
    "") + " " + df["last_name"].fillna("")
df["full_name"] = df["full_name"].str.strip()

# Remove original columns
df = df.drop(columns=["first_name", "last_name"])

# Convert date
df["subscription_date"] = pd.to_datetime(
    df["subscription_date"], errors="coerce"
).dt.date

cur = conn.cursor()

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO customers VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
    """, (
        row.idx,
        row.customer_id,
        row.full_name,
        row.company,
        row.city,
        row.country,
        row.phone1,
        row.phone2,
        row.email,
        row.subscription_date,
        row.website
    ))

conn.commit()
cur.close()
conn.close()

print("CSV loaded with merged full_name (first + last removed)")
