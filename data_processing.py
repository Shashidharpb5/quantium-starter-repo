import pandas as pd

df = pd.read_csv("data/daily_sales_data_0.csv")  # remove the 'names' parameter
print(df.head())

# Filter for only "pink morsel" rows
df = df[df["product"] == "pink morsel"]

# Remove $ from price and convert to float
df["price"] = df["price"].str.replace("$", "").astype(float)

# Convert quantity to int (just in case)
df["quantity"] = df["quantity"].astype(int)

# Convert date to datetime format
df["date"] = pd.to_datetime(df["date"])

# Calculate sales column
df["sales"] = df["price"] * df["quantity"]

# Split data based on cutoff date
cutoff_date = pd.Timestamp("2021-01-15")
before = df[df["date"] < cutoff_date]["sales"].sum()
after = df[df["date"] >= cutoff_date]["sales"].sum()

# Output results
print("\n=== Pink Morsel Sales Comparison ===")
print(f"Total sales BEFORE 15 Jan 2021: ${before:.2f}")
print(f"Total sales AFTER  15 Jan 2021: ${after:.2f}")
