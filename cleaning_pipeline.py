
import pandas as pd
import numpy as np


def clean_agent_data(txns, agents):
    """
    Clean agent transactions and merge agent reference data.

    Returns:
        clean_df: Cleaned transactions with agent information.
        log: List of cleaning actions and affected row counts.
    """
    log = []
    clean_df = txns.copy()
    agents_df = agents.copy()

    # 1. Remove duplicate transaction IDs
    duplicates = int(clean_df.duplicated(subset=["txn_id"]).sum())
    clean_df = clean_df.drop_duplicates(subset=["txn_id"]).copy()
    log.append(f"Removed {duplicates} duplicate transaction IDs")

    # 2. Standardise transaction types
    original_types = clean_df["txn_type"].copy()

    clean_df["txn_type"] = (
        clean_df["txn_type"]
        .astype("string")
        .str.strip()
        .str.lower()
        .map({
            "deposit": "Deposit",
            "withdrawal": "Withdrawal"
        })
    )

    invalid_types = int(clean_df["txn_type"].isna().sum())
    changed_types = int(
        (original_types.astype("string") != clean_df["txn_type"])
        .fillna(False)
        .sum()
    )

    log.append(f"Standardised {changed_types} transaction types")
    log.append(f"Found {invalid_types} invalid transaction types")

    # Keep only valid transaction types
    clean_df = clean_df.dropna(subset=["txn_type"]).copy()

    # 3. Convert amounts to numeric
    clean_df["amount"] = pd.to_numeric(
        clean_df["amount"]
        .astype("string")
        .str.replace(",", "", regex=False)
        .str.strip(),
        errors="coerce"
    )

    # Flag missing or invalid amounts before imputation
    clean_df["amount_imputed"] = clean_df["amount"].isna()
    missing_amounts = int(clean_df["amount_imputed"].sum())

    median_amount = clean_df["amount"].median()

    if pd.isna(median_amount):
        raise ValueError("Cannot impute amounts: no valid numeric values")

    # 4. Detect outliers before imputation
    q1 = clean_df["amount"].quantile(0.25)
    q3 = clean_df["amount"].quantile(0.75)
    iqr = q3 - q1

    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr

    clean_df["is_outlier"] = (
        (clean_df["amount"] < lower_fence) |
        (clean_df["amount"] > upper_fence)
    ).fillna(False)

    outliers = int(clean_df["is_outlier"].sum())

    # Impute missing amounts with median
    clean_df["amount"] = clean_df["amount"].fillna(median_amount)

    log.append(f"Imputed {missing_amounts} missing or invalid amounts")
    log.append(f"Flagged {outliers} amount outliers for review")

    # 5. Standardise dates
    clean_df["txn_date"] = pd.to_datetime(
        clean_df["txn_date"]
        .astype("string")
        .str.strip()
        .str.replace("/", "-", regex=False),
        errors="coerce",
        format="mixed"
    )

    invalid_dates = int(clean_df["txn_date"].isna().sum())
    log.append(f"Found {invalid_dates} invalid transaction dates")

    # 6. Prepare agent IDs for merging
    clean_df["agent_id"] = (
        clean_df["agent_id"].astype("string").str.strip()
    )

    agents_df["agent_id"] = (
        agents_df["agent_id"].astype("string").str.strip()
    )

    # Avoid multiplying transactions during the merge
    if agents_df["agent_id"].duplicated().any():
        raise ValueError("Duplicate agent IDs found in agent reference data")

    # 7. Left join preserves all remaining transactions
    rows_before_merge = len(clean_df)

    clean_df = clean_df.merge(
        agents_df,
        on="agent_id",
        how="left",
        validate="many_to_one",
        indicator=True
    )

    rows_after_merge = len(clean_df)
    unknown_agents = int((clean_df["_merge"] == "left_only").sum())

    if rows_before_merge != rows_after_merge:
        raise ValueError("Merge changed the transaction row count")

    log.append(
        f"Merge preserved {rows_before_merge} transactions; "
        f"{unknown_agents} have unknown agents"
    )

    clean_df = clean_df.drop(columns=["_merge"])

    # ISO date formatting for CSV output
    clean_df["txn_date"] = clean_df["txn_date"].dt.strftime("%Y-%m-%d")

    return clean_df, log
