import pandas as pd


def load_enrollments(file_path):
    df = pd.read_csv(file_path)
    df = df.drop(columns=["enrolled_date"])
    return df[["enrollment_id", "course_id", "learner_id", "completion_pct", "fee_paid"]]


def clean_enrollment_data(df):
    df = df.drop_duplicates(subset=["enrollment_id"],keep="first")
    #df = df[df["fee_paid"]>0]
    df = df.dropna(subset=["fee_paid"])
    return df.reset_index(drop=True)


def merge_with_courses(enrollments_df,ref_file_path):
    df2 = pd.read_csv(ref_file_path)
    enrollments_df = enrollments_df.merge(df2,on="course_id",how="inner")
    return enrollments_df


def add_revenue_realized_column(df):
    df["revenue_realized"] = (df["fee_paid"]*df["completion_pct"])/100
    return df.round(2)

def aggregate_by_track(df):
    df = df.groupby("track").agg({
        "revenue_realized":"sum",
        "completion_pct":"mean",
        "enrollment_id":"count",
    }).reset_index()

    df["completion_pct"] = df["completion_pct"].round(2)
    return df


def finalize_summary(df):
    df = df.rename(
        columns={
            "revenue_realized":"total_revenue_realized",
            "completion_pct":"avg_completion_pct",
            "enrollment_id":"enrollment_count"
        }
    )

    df = df.sort_values("track").reset_index(drop=True)
    return df[["track","total_revenue_realized","avg_completion_pct","enrollment_count"]]


if __name__ == "__main__":
    from pathlib import Path

    data_dir = Path(__file__).resolve().parent.parent / "data"
    enrollments_path = data_dir / "enrollments.csv"
    courses_path = data_dir / "courses.csv"

    df = load_enrollments(enrollments_path)
    df = clean_enrollment_data(df)
    df = merge_with_courses(df, courses_path)
    df = add_revenue_realized_column(df)
    df = aggregate_by_track(df)
    df = finalize_summary(df)
    print(df)
