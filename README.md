# Agent Data Cleanup — PLP Data Analysis Assignment 4

## Project Overview

This project demonstrates a reusable Python data-cleaning pipeline for mobile-money agent transactions.

The pipeline uses pandas and NumPy to clean transaction records, assess data quality, merge agent information, and produce county-level and weekly summaries.

## Data Cleaning Operations

- Remove duplicate transaction IDs.
- Standardise transaction types.
- Convert transaction amounts to numeric values.
- Flag and impute missing amounts using the median.
- Identify potential outliers using the IQR method.
- Standardise transaction dates.
- Merge transactions with agent records using a validated left join.
- Generate a data-quality audit log.

## Project Files

- `generate_data.py` — Original assignment dataset generator.
- `cleaning_pipeline.py` — Reusable cleaning function.
- `agent_cleanup.ipynb` — Analysis, validation, summaries, and Data Quality Report.
- `outputs/agent_transactions_clean.csv` — Cleaned transaction dataset.
- `requirements.txt` — Required Python libraries.

## Installation

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

## Regenerate the Data

Run the original dataset generator:

```bash
python generate_data.py
```

Then open `agent_cleanup.ipynb` and run all cells from top to bottom to clean the generated data and reproduce the analysis.

## Before and After Row Counts

| Stage                      | Transactions |
| -------------------------- | -----------: |
| Raw test data              |            2 |
| Cleaned test data          |            2 |
| Transactions removed       |            0 |
| Unknown-agent transactions |            0 |

These counts describe temporary test data. Replace them with the official dataset results before submission.

## Data Quality

The project evaluates six data-quality dimensions:

1. Completeness
2. Validity
3. Accuracy
4. Consistency
5. Uniqueness
6. Timeliness

## Privacy and Reproducibility

Raw generated CSV files are excluded from version control. The cleaned output and notebook results are intended to be reproducible using the original dataset generator.

## Assignment Status

The pipeline and analysis have been tested with a small sample dataset. The official seed-44 dataset generator and final validation remain outstanding.
