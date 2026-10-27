import os
import sys

# Add src folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from data_cleaning import (
    load_data,
    clean_data,
    save_cleaned_data
)

from analysis import generate_summary

from visualization import (
    plot_product_revenue,
    plot_sales_trend,
    plot_revenue_distribution
)


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_DATA = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "sales_dataset.csv"
)

CLEANED_DATA = os.path.join(
    BASE_DIR,
    "data",
    "cleaned",
    "cleaned_sales_dataset.csv"
)

GRAPH_DIR = os.path.join(
    BASE_DIR,
    "outputs",
    "graphs"
)

RESULT_DIR = os.path.join(
    BASE_DIR,
    "outputs",
    "results"
)


# ============================================================
# CREATE REQUIRED DIRECTORIES
# ============================================================

os.makedirs(
    os.path.dirname(CLEANED_DATA),
    exist_ok=True
)

os.makedirs(
    GRAPH_DIR,
    exist_ok=True
)

os.makedirs(
    RESULT_DIR,
    exist_ok=True
)


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("=" * 70)
    print("        SALES DATA ANALYSIS AND BUSINESS INSIGHTS")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. CHECK DATASET
    # --------------------------------------------------------

    print("\n[1/5] Checking dataset...")

    if not os.path.exists(RAW_DATA):
        print("\nERROR: Sales dataset not found!")
        print(f"Expected location:\n{RAW_DATA}")
        print("\nPlease place sales_dataset.csv inside:")
        print("data/raw/")
        return

    print("Dataset found successfully!")

    # --------------------------------------------------------
    # 2. LOAD DATA
    # --------------------------------------------------------

    print("\n[2/5] Loading dataset...")

    df = load_data(RAW_DATA)

    print("Dataset loaded successfully!")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nOriginal Dataset:")
    print(df.head())

    # --------------------------------------------------------
    # 3. CLEAN DATA
    # --------------------------------------------------------

    print("\n[3/5] Cleaning dataset...")

    print("\nMissing values before cleaning:")
    print(df.isnull().sum())

    df_clean = clean_data(df)

    print("\nDataset cleaned successfully!")

    print(f"Rows after cleaning: {df_clean.shape[0]}")
    print(f"Columns after cleaning: {df_clean.shape[1]}")

    print("\nMissing values after cleaning:")
    print(df_clean.isnull().sum())

    # Save cleaned dataset
    save_cleaned_data(
        df_clean,
        CLEANED_DATA
    )

    # --------------------------------------------------------
    # 4. ANALYSIS
    # --------------------------------------------------------

    print("\n[4/5] Performing sales analysis...")

    summary = generate_summary(df_clean)

    print("\n" + "-" * 60)
    print("SALES ANALYSIS RESULTS")
    print("-" * 60)

    for key, value in summary.items():

        if isinstance(value, float):
            print(f"{key}: {value:,.2f}")

        else:
            print(f"{key}: {value}")

    # --------------------------------------------------------
    # 5. VISUALIZATION
    # --------------------------------------------------------

    print("\n[5/5] Generating visualizations...")

    # Revenue by Product
    plot_product_revenue(
        df_clean,
        os.path.join(
            GRAPH_DIR,
            "revenue_by_product.png"
        )
    )

    # Sales Trend
    plot_sales_trend(
        df_clean,
        os.path.join(
            GRAPH_DIR,
            "sales_trend.png"
        )
    )

    # Revenue Distribution
    plot_revenue_distribution(
        df_clean,
        os.path.join(
            GRAPH_DIR,
            "revenue_distribution.png"
        )
    )

    print("\nGraphs generated successfully!")

    # --------------------------------------------------------
    # FINAL MESSAGE
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("        SALES EDA PROJECT COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print("\nGenerated files:")

    print(f"\nCleaned Dataset:")
    print(CLEANED_DATA)

    print("\nGraphs:")
    print(os.path.join(
        GRAPH_DIR,
        "revenue_by_product.png"
    ))

    print(os.path.join(
        GRAPH_DIR,
        "sales_trend.png"
    ))

    print(os.path.join(
        GRAPH_DIR,
        "revenue_distribution.png"
    ))

    print("\n" + "=" * 70)


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()