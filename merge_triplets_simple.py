"""
Simple merge of triplet image URLs into weight data.

- Matches on the basename of image files (after removing "-original")
- Adds columns: image_url, depth_url, normal_url
- Saves merged CSV next to the input files
"""

import pandas as pd
from pathlib import Path


# ==== 1. File paths (edit if needed) ====
TRIPLETS_CSV = "triplets_by_basename.csv"
WEIGHT_CSV = "weight_data_cleaned_sample_ready_20250604.csv"
OUT_CSV = "weight_with_triplets.csv"


# ==== 2. Helper: normalize basenames ====
def normalize_basename(x: str) -> str:
    """Extract a normalized key (remove path, extension, and '-original')."""
    if pd.isna(x):
        return ""
    name = str(x).split("/")[-1].split("\\")[-1]
    if "." in name:
        name = ".".join(name.split(".")[:-1])
    if name.lower().endswith("-original"):
        name = name[: -len("-original")]
    return name


# ==== 3. Load CSVs ====
triplets = pd.read_csv(TRIPLETS_CSV)
weight = pd.read_csv(WEIGHT_CSV)

# ==== 4. Prepare join keys ====
triplets["key"] = triplets["basename"].apply(normalize_basename)
weight["key"] = weight["00_MSG_01_IMAGE"].apply(normalize_basename)

# ==== 5. Merge ====
merged = weight.merge(
    triplets[["key", "image_url", "depth_url", "normal_url"]],
    on="key",
    how="left"
)

# ==== 6. Save result ====
merged.to_csv(OUT_CSV, index=False)

# ==== 7. Print summary ====
total = len(merged)
matched = merged["depth_url"].notna().sum()
print(f"✅ Merged successfully! Saved to: {OUT_CSV}")
print(f"   Total rows: {total}")
print(f"   Matched triplets: {matched}")
print(f"   Unmatched: {total - matched}")

# optional: show a small preview
print("\nPreview:")
print(merged[["00_MSG_01_IMAGE", "image_url", "depth_url", "normal_url"]].head())