# ecc3479-project
Emperical Project for ECC3479

ECC3479-PROJECT/
Repository Structure
│
├── code/
│   └── clean_data.py               # Script that cleans and merges raw datasets
│
├── data/
│   ├── raw/                        # Raw input datasets (not modified)
│   │   ├── petrol_prices_raw.csv
│   │   └── vic_transport_patronage_raw.csv
│   │
│   ├── clean/                      # Cleaned and analysis-ready datasets
│   │   ├── merged_transport_petrol.csv
│   │   └── codebook/               # Codebook folder
│   │       └── codebook.md
│   │
│   └── README.data                 # Instructions for obtaining raw data
│
├── output/                         # (Optional) Plots, regression outputs, tables
│
└── README.md                       # Project documentation

Getting Started

-1 Create and activate a Python environment.
You may use venv, conda, or any environment tool.

-2 Install required packages.
This project only requires pandas:
pip install pandas

-3 - Ensure raw data is available.
Place the following files into data/raw/:
- petrol_prices_raw.csv
- vic_transport_patronage_raw.csv
-!!-  see data/README.data for download instructions.!!

-4 - Run the cleaning script.
From the project root directory (ECC3479-PROJECT), run:
python code/clean_data.py

This script performs the full data‑cleaning pipeline required to transform the raw datasets into an analysis‑ready format. Specifically, it:
- Loads the raw petrol price data from data/raw/petrol_prices_raw.csv
- Parses the year-month string into a proper monthly datetime variable
- Renames variables for consistency
- Loads the raw transport patronage data from data/raw/vic_transport_patronage_raw.csv
- Combines the separate Year and Month columns into a single datetime variable
- Ensures all transport modes are preserved
- Creates a shared monthly key (Month) used to merge the two datasets
- This ensures both datasets align perfectly on the same time periods
- Merges the petrol and transport datasets into a single panel
- Each row represents one month
- Includes petrol price and all patronage variables
- Exports the final cleaned dataset to:
data/clean/merged_transport_petrol.csv

If the script runs successfully, you will see:
Merged dataset created successfully.

This confirms that the entire workflow has executed correctly and that the repository is fully reproducible.

- 5 Review the cleaned dataset.
Open:
data/clean/merged_transport_petrol.csv
- A full description of variables is provided in:
data/clean/codebook/codebook.md





