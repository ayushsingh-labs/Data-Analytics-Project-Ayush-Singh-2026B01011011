"""
PROJECT: Online Store Sales - Data Cleaning & Analysis
Tools used: Python, NumPy, pandas

Steps:
  1. Create / load raw (messy) data
  2. Inspect the data
  3. Clean the data
  4. Analyze the data
  5. Save cleaned data + print conclusions
"""

import os
import numpy as np
import pandas as pd

os.makedirs("data", exist_ok=True)


np.random.seed(42)
n = 500

categories = ["Electronics", "Clothing", "Grocery", "Books", "Home"]
base_price = {"Electronics": 15000, "Clothing": 1200, "Grocery": 300,
              "Books": 400, "Home": 2500}
cities = ["Delhi", "Mumbai", "Bengaluru", "Kolkata", "Chennai", "Ghaziabad"]

cat = np.random.choice(categories, n)
price = np.array([base_price[c] for c in cat]) * np.random.uniform(0.8, 1.2, n)
dates = pd.to_datetime("2025-01-01") + pd.to_timedelta(np.random.randint(0, 365, n), unit="D")

raw = pd.DataFrame({
    "order_id": np.arange(1001, 1001 + n),
    "order_date": dates.strftime("%d-%m-%Y"),
    "city": np.random.choice(cities, n),
    "category": cat,
    "quantity": np.random.randint(1, 6, n).astype(float),
    "unit_price": np.round(price).astype(int).astype(str),
    "discount_pct": np.random.choice([0, 5, 10, 15, 20], n).astype(float),
    "rating": np.random.randint(1, 6, n).astype(float),
})

# ---- Add "dirt" on purpose ----
idx = np.random.choice(n, 40, replace=False)
raw.loc[idx[:15], "city"] = raw.loc[idx[:15], "city"].str.upper()            # DELHI
raw.loc[idx[15:30], "city"] = " " + raw.loc[idx[15:30], "city"].str.lower() + " "  # " mumbai "
raw.loc[idx[30:35], "city"] = "Bangalore"                                    # different name
raw.loc[idx[35:40], "category"] = raw.loc[idx[35:40], "category"].str.lower()
raw.loc[np.random.choice(n, 30, replace=False), "quantity"] = np.nan         # missing
raw.loc[np.random.choice(n, 40, replace=False), "discount_pct"] = np.nan     # missing
raw.loc[np.random.choice(n, 35, replace=False), "rating"] = np.nan           # missing
raw.loc[np.random.choice(n, 3, replace=False), "rating"] = 99                # invalid
raw.loc[np.random.choice(n, 4, replace=False), "quantity"] = 500             # outlier
raw.loc[np.random.choice(n, 3, replace=False), "unit_price"] = "-500"        # invalid
p = np.random.choice(n, 40, replace=False)
raw.loc[p, "unit_price"] = "Rs. " + raw.loc[p, "unit_price"]                 # text in numbers
raw.loc[np.random.choice(n, 5, replace=False), "order_date"] = "not available"
raw = pd.concat([raw, raw.sample(15, random_state=1)], ignore_index=True)    # duplicates

raw.to_csv("data/raw_sales_data.csv", index=False)
print("Raw data saved as data/raw_sales_data.csv")

# =====================================================================
# STEP 2: INSPECT THE DATA
# =====================================================================
df = pd.read_csv("data/raw_sales_data.csv")

print("\n========== STEP 2: INSPECTION ==========")
print("Shape (rows, columns):", df.shape)
print("\nFirst 5 rows:\n", df.head())
print("\nData types:\n", df.dtypes)
print("\nMissing values per column:\n", df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())
print("\nUnique cities (before cleaning):", sorted(df["city"].unique()))

rows_before = len(df)

# =====================================================================
# STEP 3: DATA CLEANING
# =====================================================================
print("\n========== STEP 3: CLEANING ==========")

# 3.1 Remove duplicate rows
df = df.drop_duplicates()
print("3.1 Duplicates removed. Rows now:", len(df))

# 3.2 Standardize text (spaces, upper/lower case, different spellings)
df["city"] = df["city"].str.strip().str.title()
df["city"] = df["city"].replace({"Bangalore": "Bengaluru"})
df["category"] = df["category"].str.strip().str.title()
print("3.2 Cities after cleaning:", sorted(df["city"].unique()))

# 3.3 Fix price column (remove "Rs. " and convert to number)
df["unit_price"] = df["unit_price"].astype(str).str.replace(r"[^0-9\-.]", "", regex=True)
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
print("3.3 unit_price converted to numeric:", df["unit_price"].dtype)

# 3.4 Convert date column to real dates (bad values become NaT)
df["order_date"] = pd.to_datetime(df["order_date"], format="%d-%m-%Y", errors="coerce")
print("3.4 Invalid dates found:", df["order_date"].isnull().sum())

# 3.5 Handle invalid values
df = df[df["unit_price"] > 0]                       # negative price is impossible
df.loc[~df["rating"].between(1, 5), "rating"] = np.nan   # rating must be 1-5
print("3.5 Removed negative prices, invalid ratings set to NaN")

# 3.6 Handle outliers in quantity using IQR method
q1, q3 = df["quantity"].quantile(0.25), df["quantity"].quantile(0.75)
iqr = q3 - q1
upper_limit = q3 + 1.5 * iqr
print(f"3.6 Quantity outlier limit = {upper_limit}; outliers found =", (df["quantity"] > upper_limit).sum())
df["quantity"] = np.where(df["quantity"] > upper_limit, upper_limit, df["quantity"])

# 3.7 Handle missing values
df = df.dropna(subset=["order_date"])                          # date is essential -> drop
df["quantity"] = df["quantity"].fillna(df["quantity"].median())  # median for numbers
df["discount_pct"] = df["discount_pct"].fillna(0)              # no info = no discount
df["rating"] = df["rating"].fillna(df.groupby("category")["rating"].transform("median"))
print("3.7 Missing values after filling:\n", df.isnull().sum())

# 3.8 Fix data types
df["quantity"] = df["quantity"].astype(int)
df["rating"] = df["rating"].round().astype(int)

# 3.9 Create new useful columns
df["total_amount"] = df["quantity"] * df["unit_price"] * (1 - df["discount_pct"] / 100)
df["month"] = df["order_date"].dt.month_name()
df["order_size"] = np.where(df["total_amount"] >= 20000, "Large",
                    np.where(df["total_amount"] >= 5000, "Medium", "Small"))

df = df.reset_index(drop=True)
print(f"\nRows before cleaning: {rows_before} | Rows after cleaning: {len(df)}")

# =====================================================================
# STEP 4: ANALYSIS
# =====================================================================
print("\n========== STEP 4: ANALYSIS ==========")

# 4.1 Overall numbers
total_revenue = df["total_amount"].sum()
print(f"\n4.1 Total revenue: Rs. {total_revenue:,.0f}")
print(f"    Average order value: Rs. {df['total_amount'].mean():,.0f}")
print(f"    Median order value : Rs. {np.median(df['total_amount']):,.0f}")
print(f"    Std deviation      : Rs. {np.std(df['total_amount']):,.0f}")

# 4.2 Revenue by category
cat_rev = df.groupby("category")["total_amount"].sum().sort_values(ascending=False)
print("\n4.2 Revenue by category:\n", cat_rev.round(0))

# 4.3 Revenue by city
city_rev = df.groupby("city")["total_amount"].sum().sort_values(ascending=False)
print("\n4.3 Revenue by city:\n", city_rev.round(0))

# 4.4 Monthly revenue trend
month_order = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]
monthly = df.groupby("month")["total_amount"].sum().reindex(month_order)
print("\n4.4 Monthly revenue:\n", monthly.round(0))
print("    Best month :", monthly.idxmax())
print("    Worst month:", monthly.idxmin())

# 4.5 Average rating by category
print("\n4.5 Average rating by category:\n", df.groupby("category")["rating"].mean().round(2))

# 4.6 Top 5 biggest orders
print("\n4.6 Top 5 orders:\n",
      df.nlargest(5, "total_amount")[["order_id", "city", "category", "total_amount"]])

# 4.7 Order size distribution
print("\n4.7 Order size counts:\n", df["order_size"].value_counts())

# 4.8 Pivot table: city vs category
pivot = pd.pivot_table(df, values="total_amount", index="city",
                       columns="category", aggfunc="sum", fill_value=0)
print("\n4.8 Pivot table (city x category):\n", pivot.round(0))

# 4.9 Correlation (NumPy / pandas)
print("\n4.9 Correlation matrix:\n",
      df[["quantity", "unit_price", "discount_pct", "rating", "total_amount"]].corr().round(2))

# =====================================================================
# STEP 5: SAVE CLEAN DATA + CONCLUSIONS
# =====================================================================
df.to_csv("data/clean_sales_data.csv", index=False)
print("\nClean data saved as data/clean_sales_data.csv")

print("\n========== CONCLUSIONS ==========")
print(f"1. '{cat_rev.index[0]}' earns the most revenue (Rs. {cat_rev.iloc[0]:,.0f}).")
print(f"2. '{city_rev.index[0]}' is the top city by revenue.")
print(f"3. '{monthly.idxmax()}' is the best month and '{monthly.idxmin()}' the weakest.")
print(f"4. {len(df)} clean orders remain out of {rows_before} raw rows.")
print("5. Recommendation: focus marketing on the top category/city and run offers in the weakest month.")
