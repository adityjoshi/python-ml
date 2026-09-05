import pandas as pd


def load_orders(file_path):
    df = pd.read_csv(file_path)
    df = df.drop(columns=["order_date"])
    return df[["order_id", "item_id", "cafe_id", "quantity", "unit_price"]]


def remove_invalid_orders(df):
    df = df.drop_duplicates(subset=["order_id"], keep="first")
    df = df.dropna(subset=["quantity"])
    df = df[df["quantity"] > 0]
    return df


def attach_item_details(df, ref_file_path):
    items = pd.read_csv(ref_file_path)
    return df.merge(items, on="item_id", how="inner")


def add_order_value_column(df):
    df = df.copy()
    df["order_value"] = (df["quantity"] * df["unit_price"]).round(2)
    return df


def summarize_by_category(df):
    summary = (
        df.groupby("category")
        .agg({"order_value": "sum", "quantity": "mean", "order_id": "count"})
        .reset_index()
    )
    summary["quantity"] = summary["quantity"].round(2)
    return summary.reset_index(drop=True)


def format_summary(df):
    df = df.rename(
        columns={
            "order_value": "total_revenue",
            "quantity": "avg_quantity",
            "order_id": "order_count",
        }
    )
    df = df.sort_values("category").reset_index(drop=True)
    return df[["category", "total_revenue", "avg_quantity", "order_count"]]


if __name__ == "__main__":
    from pathlib import Path

    data_dir = Path(__file__).resolve().parent.parent / "data"
    orders_path = data_dir / "orders.csv"
    items_path = data_dir / "items.csv"

    df = load_orders(orders_path)
    df = remove_invalid_orders(df)
    df = attach_item_details(df, items_path)
    df = add_order_value_column(df)
    df = summarize_by_category(df)
    df = format_summary(df)
    print(df)
