"""
Simple ETL script
Extracts data from a CSV, transforms it, and loads it into another CSV.
"""

import pandas as pd


def extract(input_file: str) -> pd.DataFrame:
    """Extract data from CSV."""
    return pd.read_csv(input_file)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Transform data by cleaning and adding new features."""
    # Drop rows with missing values
    df = df.dropna()

    # Add uppercase/lowercase columns if 'name' exists
    if "name" in df.columns:
        df["name_upper"] = df["name"].str.upper()
        df["name_lower"] = df["name"].str.lower()
        # Moderate transformation: name length
        df["name_length"] = df["name"].str.len()

    # Normalize numeric columns (0-1 scaling)
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    for col in numeric_cols:
        min_val = df[col].min()
        max_val = df[col].max()
        if max_val != min_val:
            df[col + "_norm"] = (df[col] - min_val) / (max_val - min_val)
        else:
            df[col + "_norm"] = 0  # avoid division by zero

    # Optional: filter rows where 'amount' > 0 if exists
    if "amount" in df.columns:
        df = df[df["amount"] > 0]

    return df


def load(df: pd.DataFrame, output_file: str):
    """Load data into a new CSV."""
    df.to_csv(output_file, index=False)


# New function added
def load_csv_to_dataframe(file_path: str) -> pd.DataFrame:
  
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded {len(df)} rows from {file_path}")
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()  # return empty DataFrame on error


if __name__ == "__main__":
    input_path = "data/input.csv"
    output_path = "data/output.csv"

    # Run ETL
    print("Hello Github Actions!")
    print("******")

    data = extract(input_path)
    transformed = transform(data)
    load(transformed, output_path)

    # Optional: use new helper function to reload CSV
    reloaded = load_csv_to_dataframe(output_path)
    print("🔹 ETL process completed.")
