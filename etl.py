"""
Simple ETL script
Extracts data from a CSV, transforms it, and loads it into another CSV.
"""

import pandas as pd


def extract(input_file: str) -> pd.DataFrame:
    """Extract data from CSV."""
    return pd.read_csv(input_file)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Transform data by cleaning and adding a new column."""
    # Drop rows with missing values
    df = df.dropna()

    # Add a new column with uppercase names if 'name' exists
    if "name" in df.columns:
        df["name_upper"] = df["name"].str.upper()
        df["name_lower"] = df["name"].str.lower()

    return df


def load(df: pd.DataFrame, output_file: str):
    """Load data into a new CSV."""
    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    input_path = "data\input.csv"
    output_path = "data\output.csv"

    # Run ETL
    print("Hello Github Actions!")
    print("🔹 Starting ETL process...")
    print("----------------")

    data = extract(input_path)
    transformed = transform(data)
    load(transformed, output_path)

