import pandas as pd


def load_data(file_path):
    """Load sales data from a CSV file."""
    df = pd.read_csv(file_path)
    return df


def clean_data(df):
    """Clean and prepare the sales dataset."""

    # Remove duplicate records
    df = df.drop_duplicates()

    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Convert numerical columns
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce")

    # Remove rows with missing important values
    df = df.dropna(
        subset=["Date", "Product", "Quantity", "Revenue"]
    )

    # Remove invalid values
    df = df[df["Quantity"] >= 0]
    df = df[df["Revenue"] >= 0]

    # Sort by date
    df = df.sort_values("Date")

    # Reset index
    df = df.reset_index(drop=True)

    return df


def save_cleaned_data(df, output_path):
    """Save cleaned data to a CSV file."""
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to: {output_path}")