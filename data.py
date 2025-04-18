import pandas as pd
import numpy as np
from scipy.stats import zscore
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

def clean_cancer_data():
    file_path = 'cancer.csv'
    df = pd.read_csv(file_path)

    print("data samples...")
    print(df.head())

    print('Clean column names')
    df.columns = df.columns.str.strip()

    drop_cols = [col for col in df.columns if "CI*Rank" in col or col.startswith("Lower CI") or col.startswith("Upper CI")]
    print(f"dropping the following columns {drop_cols}")
    df = df.drop(columns=drop_cols)

    numeric_cols = [
        "Age-Adjusted Incidence Rate([rate note]) - cases per 100,000",
        "Lower 95% Confidence Interval",
        "Upper 95% Confidence Interval",
        "Average Annual Count",
        "Recent 5-Year Trend ([trend note]) in Incidence Rates"
    ]
    print("getting rid of commas in numeric columns")
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "").str.strip(), errors='coerce')

    df['County'] = df['County'].astype(str)
    df['State'] = df['County'].str.extract(r",\s*([A-Za-z ]+)\(")[0]
    df['County'] = df['County'].str.extract(r"^\"?([^,]+)")[0]

    print("\n printing cleaned data samples...")
    print(df.head())

    df = df.dropna(subset=["Age-Adjusted Incidence Rate([rate note]) - cases per 100,000"])

    df = df.rename(columns={
        "Age-Adjusted Incidence Rate([rate note]) - cases per 100,000": "IncidenceRate",
        "2023 Rural-Urban Continuum Codes([rural urban note])": "RuralUrban",
        "Recent 5-Year Trend ([trend note]) in Incidence Rates": "TrendSlope",
        "Recent Trend": "Trend"
    })

    cleaned_file_path = 'cleaned_cancer_incidence_data.csv'
    df.to_csv(cleaned_file_path, index=False)
    return df

def viewCancerData(df):
    plt.figure(figsize=(10, 5))
    sns.histplot(df["IncidenceRate"], bins=30, kde=True)
    plt.title("Distribution of Cancer Incidence Rates (per 100,000)")
    plt.xlabel("Incidence Rate")
    plt.ylabel("Number of Counties")
    plt.show()

    top10 = df.sort_values("IncidenceRate", ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x="IncidenceRate", y="County", data=top10)
    plt.title("Top 10 Counties by Cancer Incidence Rate")
    plt.xlabel("Incidence Rate")
    plt.ylabel("County")
    plt.show()

    plt.figure(figsize=(8, 6))
    sns.boxplot(x="RuralUrban", y="IncidenceRate", data=df)
    plt.title("Cancer Incidence Rate by Rural/Urban Classification")
    plt.show()

def clean_airData():
    df = pd.read_csv("air_countydata.csv")
    print("data samples...")
    print(df.head())

    df.replace(["ND", "IN"], np.nan, inplace=True)

    pollutant_cols = [
        "CO          8-hr (ppm)",
        "Pb           3-mo (µg/m3)",
        "NO2         AM (ppb)",
        "NO2          1-hr (ppb)",
        "O3            8-hr (ppm)",
        "PM10        24-hr (µg/m3) ",
        "PM2.5     Wtd AM (µg/m3) ",
        "PM2.5     24-hr (µg/m3) ",
        "SO2         1-hr (ppb)"
    ]

    df.columns = df.columns.str.strip()

    for col in pollutant_cols:
        df[col.strip()] = pd.to_numeric(df[col.strip()], errors='coerce')
        print(col)

    df_clean = df.dropna(subset=[col.strip() for col in pollutant_cols], how='all')

    cleaned_file_path = 'cleaned_air_data.csv'
    df.to_csv(cleaned_file_path, index=False)
    return df


def main():
    if len(sys.argv) != 2:
        print("Usage: python data.py <dataset name>")
        sys.exit(1)

    data_name = sys.argv[1]

    print(f"Loading and cleaning {data_name} data")
    if data_name == "cancer":
       cleaned_df = clean_cancer_data()
       viewCancerData(cleaned_df)
    if data_name == "air":
       cleaned_df = clean_airData()

if __name__ == "__main__":
    main()