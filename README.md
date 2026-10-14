# Agent Data Cleanup — PLP Data Analysis Assignment 4

## Project Overview

This project implements a reusable Python data-cleaning pipeline for mobile-money agent transactions.

Using pandas and NumPy, the pipeline cleans transaction records, evaluates data quality, merges agent information, and produces county-level and weekly transaction summaries.

The pipeline processed **1,015 raw transaction records and produced 1,000 cleaned records**, removing 15 duplicate transaction IDs.

## Data Cleaning Operations

- Remove duplicate transaction IDs.
- Standardise transaction types to `Deposit` and `Withdrawal`.
- Convert transaction amounts into numeric values.
- Identify missing or invalid amounts and impute them using the median.
- Flag potential amount outliers using the interquartile range (IQR) method.
- Standardise transaction dates to ISO format (`YYYY-MM-DD`).
- Merge transactions with agent records using a validated left join.
- Preserve transactions with unknown agent IDs for further investigation.
- Generate a data-quality audit table and cleaning log.

## Project Files

- `generate_data.py` — Temporary seed-44 dataset generator used for testing.
- `cleaning_pipeline.py` — Reusable cleaning function `clean_agent_data(txns, agents)`.
- `agent_cleanup.ipynb` — Data cleaning, audit, validation, county summaries, weekly pivot table, and Data Quality Report.
- `outputs/agent_transactions_clean.csv` — Cleaned transaction dataset.
- `requirements.txt` — Required Python libraries.
- `.gitignore` — Excludes raw generated datasets and temporary files.

## Installation

Install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

## Regenerate the Data

Run the temporary seed-44 dataset generator:

```bash
python generate_data.py
```

This creates the raw transaction and agent datasets inside the `data/` directory.

Next, open `agent_cleanup.ipynb` in Jupyter Notebook or VS Code.

Restart the kernel and run all cells from top to bottom to reproduce the cleaning process, data-quality audit, validation checks, county summary, weekly pivot table, and cleaned CSV output.

## Before and After Row Counts

| Processing stage                  | Number of transactions |
| --------------------------------- | ---------------------: |
| Raw transactions ingested         |                  1,015 |
| Duplicate transaction IDs removed |                     15 |
| Cleaned transactions exported     |                  1,000 |
| Transactions with unknown agents  |                     10 |

The cleaning pipeline reduced the dataset from **1,015 raw records to 1,000 cleaned records** by removing 15 duplicate transaction IDs.

The validated agent merge preserved all 1,000 cleaned transactions, including 10 transactions with unmatched agent IDs.

## Data Quality Assessment

The project evaluates six data-quality dimensions:

1. **Completeness:** Identifies missing or invalid values and applies median imputation where appropriate.
2. **Validity:** Standardises transaction types, numeric amounts, and transaction dates.
3. **Accuracy:** Flags potential amount outliers using the IQR method.
4. **Consistency:** Validates agent information through a controlled left join.
5. **Uniqueness:** Removes duplicate transaction IDs.
6. **Timeliness:** Standardises transaction dates to support chronological and weekly analysis.

## Data Privacy and Reproducibility

Raw generated CSV files are excluded from version control using `.gitignore`.

The repository includes the cleaning pipeline, analysis notebook, dataset generator, and cleaned output to support reproducibility.

Transactions with unmatched agent IDs are preserved for auditing rather than automatically deleted.

## Assignment Status

The cleaning pipeline and analysis were tested using **1,015 generated transaction records**, producing **1,000 cleaned records**.

The notebook includes the data-quality audit, post-merge validation, county summary, weekly pivot table, and six-dimension Data Quality Report.

**Dataset limitation:** The original PLP-provided dataset generator was unavailable. A temporary seed-44 generator was created for testing. The results should be revalidated if the original generator becomes available.
