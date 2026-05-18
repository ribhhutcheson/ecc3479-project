# ecc3479-project
Emperical Project for ECC3479

What is the effect of changes in the average monthly petrol price on monthly public transport ridership for commuters in Melbourne between 2022 and 2025, compared with months where petrol prices remain stable? 

This project constructs a reproducible monthly dataset for metropolitan Melbourne combining petrol prices and public transport patronage. Rainfall, population and public holiday data is collected as potential control variables. All raw data is cleaned, transformed and merged in a single python script. 

Repository Structure
ECC3479-PROJECT/
│
├── code/
│   ├── clean_data.py
│   └── tables_figures.ipynb
│
├── data/
│   ├── raw/
│   │   ├── melbourne_population_change.csv
│   │   ├── melbourne_rainfall_raw.csv
│   │   ├── monthly_public_holidays.csv
│   │   ├── petrol_prices_raw.csv
│   │   └── vic_transport_patronage_raw.csv
│   │
│   └── clean/
│       ├── merged_final.csv
│       ├── merged_transport_petrol.csv
│       ├── population_monthly.csv
│       ├── public_holidays_monthly.csv
│       ├── rainfall_monthly.csv
│       └── codebook/
│
│   
│
├── README.data
│
├── output/
│    ├── figure1_timeseries.png
│    ├── figure2_coefplot.png
│    ├── main_results_table.csv
│    ├── regression_table.csv
│    ├── robustness_table.csv
│    ├── table1_summary.pdf
│    ├── table1_summary.png
│    ├── table2_main_results.png
│    └── table3_robustness.png
│ 
├── analysis.ipynb
│
├── EDA.ipynb
├── robustness.ipynb
└── README.md

Folder meanings
- data/raw/ — unmodified source data
- data/clean/ — cleaned datasets created by the pipeline
- code/ — Python scripts used to clean and merge data
- output/ — regression outputs, plots, tables
- README.data — data dictionary + variable descriptions
- README.md — project overview and reproduction instructions

Getting Started

-1 Create and activate a Python environment. (Python 3.9 or later)
You may use venv, conda, or any environment tool.

-2 Install required packages.
This project requires the following packages:
    pip install pandas statsmodels jupyter

Clone or download the repository
git clone <https://github.com/ribhhutcheson/ecc3479-project.git>
cd ecc3479-project

-3  Ensure raw data is in the correct folder
Place the following files inside data/raw/:
- melbourne_population_change.csv
- melbourne_rainfall_raw.csv
- monthly_public_holidays.csv
- petrol_prices_raw.csv
- vic_transport_patronage_raw.csv

-!!-  SEE data/README.data for download instructions.!!

-4 - Run the cleaning script.
From the project root directory (ECC3479-PROJECT), run:
python code/clean_data.py

This script performs the full data‑cleaning pipeline required to transform the raw datasets into an analysis‑ready format. Specifically, it:
1. Petrol Prices
- Loads raw petrol price data from data/raw/petrol_prices_raw.csv.
- Parses the year-month string into a proper monthly datetime variable.
- Renames columns for consistency and clarity.
- Produces a clean monthly petrol price series.

2. Transport Patronage
- Loads raw transport patronage data from data/raw/vic_transport_patronage_raw.csv.
- Combines separate Year and Month columns into a single datetime variable.
- Ensures all transport modes (train, tram, bus) are preserved.
- Produces a clean monthly patronage dataset.

3. Merge Petrol + Transport (Intermediate Dataset)
- Creates a shared monthly key (month) used to align both datasets.
- Merges petrol prices and transport patronage into a single monthly panel.
- Each row represents one month with petrol price and total patronage.
- Exports the intermediate dataset to:
data/clean/merged_transport_petrol.csv

4. Rainfall
- Loads raw rainfall data from data/raw/melbourne_rainfall_raw.csv.
- Reshapes the wide-format rainfall table into long monthly format.
- Converts month names and year columns into a proper datetime variable.
- Filters to the analysis period (2022–2026).
- Exports the cleaned rainfall dataset to:
data/clean/rainfall_monthly.csv

5. Population
- Loads quarterly population change data from data/raw/melbourne_population_change.csv.
- Parses quarterly dates and cleans numeric fields.
- Computes cumulative population levels from the Jun‑2021 ERP baseline.
- Expands quarterly population values into monthly estimates.
- Filters to the analysis period (2022–2026).
- Exports the cleaned population dataset to:
data/clean/population_monthly.csv

6. Public Holidays
- Loads monthly public holiday counts from data/raw/monthly_public_holidays.csv.
- Converts year and month columns into a proper datetime variable.
- Renames variables for clarity.
- Exports the cleaned public holiday dataset to:
data/clean/public_holidays_monthly.csv

7. Final Merge (All Control Variables)
- Loads all cleaned datasets:
- petrol + transport
- rainfall
- population
- public holidays
- Merges them sequentially on the shared month key.
- Ensures all variables align perfectly on the same monthly timeline.
- Sorts the final dataset chronologically.
- Exports the final analysis‑ready dataset to:
data/clean/merged_final.csv

If the script runs successfully, you will see:
Petrol data cleaned and saved.
Transport data cleaned and saved.
Merged petrol + transport dataset created successfully.
Rainfall cleaned and saved.
Population cleaned and saved.
Public holidays cleaned and saved.
Final merged dataset created successfully.


This confirms that the entire workflow has executed correctly and that the repository is fully reproducible.

-5 Review the cleaned dataset.
Open:
data/clean/merged_final.csv
- A full description of variables is provided in:
data/clean/codebook/codebook.md

-6 Run the EDA

Launch Jupyter Notebook from the project root:
    jupyter notebook

Open EDA.ipynb and run all cells (Kernel → Restart & Run All)

This notebook explores the analysis-ready dataset prior to regression.
It covers:
- Variable distributions- checking for skew, outliers, and data gaps
- Time series trends- visualising petrol prices and patronage over 2022–2025
- Seasonality- identifying recurring monthly patterns in ridership
  that will need to be controlled for in the regression
- Variable relationships- inspecting the raw correlation between
  petrol prices and patronage across transport modes


-7 Analysis

The primary analysis file is:
analysis.ipynb

This notebook runs end-to-end on the cleaned data and includes:
- Declaration of descriptive ambition
- Econometric specification and justification
- OLS regression with four specifications- bivariate, controls, 
  controls + seasonal FE, log-linear
- Formatted regression table
- Interpretation of main coefficients
- Assumptions
- Threats and limitations
- Conclusion and policy implications

To run the analysis:
1. Ensure you have completed the data cleaning pipeline (steps 1-5 above)
2. In the same JUpyter session open analysis.ipynb and run all cells (Kernel → Restart & Run All)

The notebook reads from:
   data/clean/merged_final.csv

And saves regression outputs to:
   output/regression_table.csv

-8 Robustness Analysis

The robustness analysis file is:
    robustness.ipynb

In the same Jupyter session, open robustness.ipynb and run all cells
(Kernel → Restart & Run All).

This notebook runs end-to-end on the cleaned data and includes:
- Restatement of main result and descriptive declaration
- Standard error justification (HC3 throughout)
- Four robustness checks:
    1. Alternative control sets (minimal, controls only, full)
    2. Alternative sample (drop 2022, restrict to 2023–2025)
    3. Alternative functional form (levels vs log)
    4. Influential observations (Cook's distance, threshold 4/N)
- Robustness table presenting all checks side-by-side
- Interpretation of each check and overall assessment

The notebook reads from:
    data/clean/merged_final.csv

And saves the robustness table to:
    output/robustness_table.csv

Note: ensure the data cleaning pipeline (steps 1–5) and primary
analysis (steps 6–7) have been completed before running this notebook.

-9 Report Replication Package

The following tables and figures appear in the PDF report. 
Each can be reproduced by running the scripts below in order.

Full Pipeline (run in order)
1. `python code/clean_data.py` — produces all cleaned datasets in data/clean/
2. `analysis.ipynb` — produces main regression results
3. `robustness.ipynb` — produces robustness checks
4. `code/tables_figures.ipynb` — produces all tables and figures for the report

Table and Figure Mapping

| Output | File | Produced by |
|--------|------|-------------|
| Table 1: Summary Statistics | output/table1_summary_stats.png | code/tables_figures.ipynb |
| Table 2: Main Results | output/table2_main_results.png | code/tables_figures.ipynb |
| Table 3: Robustness Checks | output/table3_robustness.png | code/tables_figures.ipynb |
| Figure 1: Time Series Plot | output/figure1_timeseries.png | code/tables_figures.ipynb |
| Figure 2: Coefficient Plot | output/figure2_coefplot.png | code/tables_figures.ipynb |

Notes
- All scripts assume they are run from the project root directory
- data/clean/merged_final.csv must exist before running any notebooks
- Python 3.9 or later required
- Required packages: pandas, statsmodels, numpy, matplotlib, jupyter