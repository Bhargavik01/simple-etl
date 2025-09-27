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

    # Add a new column with uppercase and lowercase names if 'name' exists
    if "name" in df.columns:
        df["name_upper"] = df["name"].str.upper()
        df["name_lower"] = df["name"].str.lower()

    return df


def load(df: pd.DataFrame, output_file: str):
    """Load data into a new CSV."""
    df.to_csv(output_file, index=False)


# New function added
def load_csv_to_dataframe(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame safely.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
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
    print("🔹 Starting ETL process...")
    print("----------------")

    data = extract(input_path)
    transformed = transform(data)
    load(transformed, output_path)

    # Optional: use new helper function to reload CSV
    reloaded = load_csv_to_dataframe(output_path)
    print("🔹 ETL process completed.")
