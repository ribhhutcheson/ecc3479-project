import pandas as pd

# File paths
petrol_path = "data/raw/petrol_prices_raw.csv"
transport_path = "data/raw/vic_transport_patronage_raw.csv"

# Load petrol data
petrol = pd.read_csv(petrol_path)

# Fix petrol column names
petrol.rename(columns={
    "year-month": "Month",
    "petrol_price": "PetrolPrice"
}, inplace=True)

# Convert "2022-01" → datetime
petrol["Month"] = pd.to_datetime(petrol["Month"], format="%Y-%m")

# Load transport data
transport = pd.read_csv(transport_path)

# Convert Year + Month → datetime
transport["Month"] = pd.to_datetime(dict(
    year=transport["Year"],
    month=transport["Month"],
    day=1
))

# Merge datasets
merged = pd.merge(transport, petrol, on="Month", how="inner")

# Save cleaned dataset
merged.to_csv("data/clean/merged_transport_petrol.csv", index=False)

print("Merged dataset created successfully.")