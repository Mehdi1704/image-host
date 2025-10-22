#!/usr/bin/env python3
"""
remove_columns.py

Remove one or more columns from a CSV file and save the result as a new file.
"""

import pandas as pd

# ==== 1. Set file paths ====
INPUT_CSV = "weight_with_triplets.csv"       # your original file
OUTPUT_CSV = "weight_without_extra_cols.csv" # file to save
COLUMNS_TO_REMOVE = ["key", "image_url"]  # edit this list


# ==== 2. Load the CSV ====
print(f"Loading {INPUT_CSV} ...")
df = pd.read_csv(INPUT_CSV)
print(f"Columns before removal: {list(df.columns)}")

# ==== 3. Drop columns safely (ignore missing ones) ====
df.drop(columns=COLUMNS_TO_REMOVE, errors="ignore", inplace=True)

# ==== 4. Save new file ====
df.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Saved cleaned CSV to {OUTPUT_CSV}")
print(f"Columns after removal: {list(df.columns)}")