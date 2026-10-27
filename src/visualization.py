import matplotlib.pyplot as plt


def plot_product_revenue(df, save_path=None):
    """Create a bar chart of revenue by product."""

    product_revenue = (
        df.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 6))

    product_revenue.plot(kind="bar")

    plt.title("Revenue by Product")
    plt.xlabel("Product")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)

    plt.show()


def plot_sales_trend(df, save_path=None):
    """Create a line chart showing sales over time."""

    daily_revenue = (
        df.groupby("Date")["Revenue"]
        .sum()
    )

    plt.figure(figsize=(12, 6))

    plt.plot(
        daily_revenue.index,
        daily_revenue.values,
        marker="o"
    )

    plt.title("Sales Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)

    plt.show()


def plot_revenue_distribution(df, save_path=None):
    """Create a pie chart showing revenue contribution by product."""

    product_revenue = (
        df.groupby("Product")["Revenue"]
        .sum()
    )

    plt.figure(figsize=(8, 8))

    product_revenue.plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Revenue Distribution by Product")
    plt.ylabel("")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)

    plt.show()