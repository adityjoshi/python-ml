import pandas as pd


def load_visit_records(file_path):
    df = pd.read_csv(file_path)
    df = df.drop(columns=["visit_date"])
    return df[["visit_id", "service_id", "clinic_id", "consultation_fee", "medicine_fee"]]


def drop_incomplete_visits(df):
    df = df.drop_duplicates(subset=["visit_id"], keep="first")
    df = df.dropna(subset=["consultation_fee", "medicine_fee"])
    return df


def attach_service_details(df, service_ref):
    df = df.merge(service_ref, on="service_id", how="inner")
    df = df.drop(columns=["service_id"])
    return df


def attach_clinic_details(df, clinic_ref):
    df = df.merge(clinic_ref, on="clinic_id", how="inner")
    df = df.drop(columns=["clinic_id"])
    return df


def add_total_bill(df):
    df = df.copy()
    df["total_bill"] = (df["consultation_fee"] + df["medicine_fee"]).round(2)
    return df


def summarize_by_city(df):
    summary = (
        df.groupby("city")
        .agg({"total_bill": "mean", "visit_id": "count"})
        .reset_index()
    )
    summary = summary.rename(
        columns={
            "total_bill": "avg_bill_amount",
            "visit_id": "visit_count",
        }
    )
    summary["avg_bill_amount"] = summary["avg_bill_amount"].round(2)
    summary = summary.sort_values(
        by=["avg_bill_amount", "city"], ascending=[False, True]
    ).reset_index(drop=True)
    return summary[["city", "avg_bill_amount", "visit_count"]]


if __name__ == "__main__":
    from pathlib import Path

    data_dir = Path(__file__).resolve().parent.parent / "data"
    visits_path = data_dir / "visits.csv"
    service_path = data_dir / "service_types.csv"
    clinic_path = data_dir / "clinics.csv"

    df = load_visit_records(visits_path)
    service_ref = pd.read_csv(service_path)
    clinic_ref = pd.read_csv(clinic_path)

    df = drop_incomplete_visits(df)
    df = attach_service_details(df, service_ref)
    df = attach_clinic_details(df, clinic_ref)
    df = add_total_bill(df)
    df = summarize_by_city(df)
    print(df)
