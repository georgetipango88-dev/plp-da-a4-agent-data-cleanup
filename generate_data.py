"""
Temporary dataset generator for testing PLP Assignment 4.

IMPORTANT:
This is NOT the original PLP Dataset-section generator.
Replace it if the official generator becomes available.
"""

from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(44)

# Generate agent reference data
counties = [
    "Nairobi", "Kiambu", "Nakuru",
    "Kisumu", "Mombasa", "Laikipia"
]

agents = pd.DataFrame({
    "agent_id": [f"A{i:03d}" for i in range(1, 51)],
    "county": rng.choice(counties, size=50)
})

# Generate transaction records
n = 1000

transactions = pd.DataFrame({
    "txn_id": [f"T{i:05d}" for i in range(1, n + 1)],
    "agent_id": rng.choice(agents["agent_id"], size=n),
    "txn_type": rng.choice(
        ["Deposit", "Withdrawal", "deposit", "withdrawal"],
        size=n
    ),
    "amount": rng.integers(100, 50000, size=n).astype(float),
    "txn_date": rng.choice(
        pd.date_range("2026-01-01", periods=90),
        size=n
    )
})

# Introduce reproducible data-quality problems
transactions.loc[10:29, "amount"] = np.nan
transactions.loc[30:39, "txn_type"] = "deposit"
transactions.loc[40:49, "txn_type"] = "withdrawal"
transactions.loc[50:59, "agent_id"] = "UNKNOWN"
transactions.loc[60:64, "amount"] = 500000

# Add duplicate transaction IDs
transactions = pd.concat(
    [transactions, transactions.iloc[:15]],
    ignore_index=True
)

# Save raw datasets
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

transactions.to_csv(
    data_dir / "agent_transactions_raw.csv",
    index=False
)

agents.to_csv(
    data_dir / "agents_raw.csv",
    index=False
)

print("Temporary datasets generated successfully!")
print("Raw transactions:", len(transactions))
print("Agents:", len(agents))
print("Seed: 44")