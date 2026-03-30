import pandas as pd

# -----------------------------
# STEP 1: CLEAN RAINFALL DATA
# -----------------------------

rain = pd.read_csv("data/raw/melbourne_rainfall_raw.csv", sep="\t")

# Fix common BoM issues
rain.columns = rain.columns.str.strip()          # remove spaces
rain.columns = rain.columns.str.replace('\ufeff', '')  # remove BOM if present

print("Columns:", rain.columns.tolist())  # debug print

# Melt Jan–Dec into long format
rain_long = rain.melt(
    id_vars=["Year"],
    value_vars=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
    var_name="Month",
    value_name="rainfall_mm"
)

rain_long = rain_long.dropna(subset=["rainfall_mm"])

rain_long["month"] = pd.to_datetime(
    rain_long["Year"].astype(str) + "-" + rain_long["Month"],
    format="%Y-%b"
)

rain_clean = rain_long[rain_long["month"] >= "2022-01"]
rain_clean = rain_clean.sort_values("month")
rain_clean = rain_clean[["month", "rainfall_mm"]]

rain_clean.to_csv("data/clean/rainfall_monthly.csv", index=False)

print("Rainfall cleaned and saved.")

# -----------------------------
# STEP 2: CLEAN POPULATION DATA
# -----------------------------

import csv

# Read the file using proper CSV parser (handles commas in numbers)
clean_rows = []

with open("data/raw/melbourne_population_change.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    
    for row in reader:
        # Skip empty rows or header/source rows
        if not row or not row[0] or "Components" in row[0] or "Source" in row[0]:
            continue
        
        # Skip the header row (first cell is empty, second is "Total growth")
        if len(row) > 1 and row[1] == "Total growth":
            continue
        
        # Only process rows with exactly 4 values
        if len(row) == 4:
            clean_rows.append([cell.strip() for cell in row])

# Convert to DataFrame
pop = pd.DataFrame(clean_rows, columns=[
    "Quarter", "Total growth", "Natural increase", "Net overseas migration"
])

print("POP COLUMNS:", pop.columns.tolist())
print(pop.head())

# Convert quarter to datetime
pop["quarter"] = pd.to_datetime(pop["Quarter"], format="%b-%y")

# Convert numeric columns (remove commas)
pop["Total growth"] = pop["Total growth"].str.replace(",", "").astype(int)
pop["Natural increase"] = pop["Natural increase"].str.replace(",", "").astype(int)
pop["Net overseas migration"] = pop["Net overseas migration"].str.replace(",", "").astype(int)

# Sort by date
pop = pop.sort_values("quarter")

# Create population level series
starting_population = 6680648  # Victoria ERP Jun-21
pop["population_level"] = starting_population + pop["Total growth"].cumsum()

# Expand quarterly → monthly
pop_months = []
for _, row in pop.iterrows():
    q_end = row["quarter"]
    months = pd.date_range(q_end - pd.offsets.MonthEnd(2), q_end, freq="ME")
    for m in months:
        pop_months.append({"month": m, "population": row["population_level"]})

pop_monthly = pd.DataFrame(pop_months)

# Filter to 2022 onwards
pop_monthly = pop_monthly[pop_monthly["month"] >= "2022-01"]

# Save cleaned population
pop_monthly.to_csv("data/clean/population_monthly.csv", index=False)

print("Population cleaned and saved.")

# -----------------------------
# STEP 3: CLEAN PUBLIC HOLIDAYS
# -----------------------------

hol = pd.read_csv("data/raw/monthly_public_holidays.csv")

# Create a proper month column (YYYY-MM-01)
hol["month"] = pd.to_datetime(
    hol["year"].astype(str) + "-" + hol["month"].astype(str) + "-01"
)

# Rename the count column to something clean
hol = hol.rename(columns={"amount of public holidays": "public_holiday_count"})

# Keep only needed columns
hol_monthly = hol[["month", "public_holiday_count"]]

# Save cleaned file
hol_monthly.to_csv("data/clean/public_holidays_monthly.csv", index=False)

print("Public holidays cleaned and saved.")

# -----------------------------
# STEP 4: MERGE PETROL + TRANSPORT
# -----------------------------
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

# -----------------------------
# STEP 5: MERGE ALL DATASETS
# -----------------------------

import pandas as pd

# Load petrol + transport (already merged earlier)
merged = pd.read_csv("data/clean/merged_transport_petrol.csv")

# merged_transport_petrol.csv has "Month" not "month"
if "month" not in merged.columns and "Month" in merged.columns:
    merged = merged.rename(columns={"Month": "month"})

merged["month"] = pd.to_datetime(merged["month"])

# Load rainfall
rain_clean = pd.read_csv("data/clean/rainfall_monthly.csv")
rain_clean["month"] = pd.to_datetime(rain_clean["month"])

# Load population
pop_monthly = pd.read_csv("data/clean/population_monthly.csv")
pop_monthly["month"] = pd.to_datetime(pop_monthly["month"])

# Load public holidays
hol_monthly = pd.read_csv("data/clean/public_holidays_monthly.csv")
hol_monthly["month"] = pd.to_datetime(hol_monthly["month"])

# Merge step-by-step
final = merged.merge(rain_clean, on="month", how="left")
final = final.merge(pop_monthly, on="month", how="left")
final = final.merge(hol_monthly, on="month", how="left")

# Sort by month for readability
final = final.sort_values("month")

# Save final dataset
final.to_csv("data/clean/merged_final.csv", index=False)

print("Final merged dataset created successfully.")