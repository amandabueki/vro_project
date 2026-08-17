"""
data_preparation.py

Functions for loading and preparing the precipitation and temperature dataset for the 
analysis of the relationship between heavy rainfall events and climate change.
"""

from pathlib import Path
import pandas as pd

# Path to the processed dataset
# Load the merged CSV data

DATA_PATH = Path("data") / "processed" / "merged_data.csv"


def load_dataset(path: Path = DATA_PATH) -> pd.DataFrame:

    print("Loading dataset...")
    df = pd.read_csv(path)
    print(f"Dataset loaded successfully ({len(df)} rows).")

    return df

# The three columns we need from the original dataset; date, precipitation amount and temperature

def select_columns(df: pd.DataFrame) -> pd.DataFrame:

    columns = ["date",
               "selected_precip_mm",
               "selected_temperature_degC"]

    return df[columns].copy()

# Changing the column names for easy usage during the project

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:

    return df.rename(columns={"date": "date",
                              "selected_precip_mm": "rain_mm",
                              "selected_temperature_degC": "temp_C"})

# Creating new columns

def create_columns(df: pd.DataFrame) -> pd.DataFrame:

    df ["rain_6_mm/h"] = df ["rain_mm"] / 4
    df ["rain_1_mm/h"] = df ["rain_mm"] / 24

    return df

# Converting the date column into pandas datetime format

def convert_date(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    # Converts the date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    return df

# Creating time-related variables

def create_time_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    # Extract year from the date
    df["year"] = df["date"].dt.year

    # Extract month
    df["month"] = df["date"].dt.month

    # Extract season (meteorological)
    df["season"] = (
        (df["month"] % 12 + 3) // 3
    )

    return df

# wurde in notebooks bereits durchgeführt
# def check_missing_values(df: pd.DataFrame) -> pd.DataFrame:

#    print("\nMissing values:")
#    print(df.isnull().sum())

#    return df

# wurde wahrscheinlich ebenso gemacht
# def dataset_info(df: pd.DataFrame) -> None:

#    print("\nDataset information")
#    print("-" * 40)
#    print(df.info())
#    print("\nFirst five rows:")
#    print(df.head())
#    print("-" * 40)

# pipeline function 

# Saving new csv with columns we need

def saving_csv(df: pd.DataFrame) -> pd.DataFrame:

    df.to_csv("data/processed/weather_data.csv", index=False)

    return df

def prepare_dataset() -> pd.DataFrame:

    df = load_dataset()

    df = select_columns(df)

    df = rename_columns(df)

    df = create_columns(df)

    df = convert_date(df)

    df = create_time_features(df)

#   df = check_missing_values(df)

#   dataset_info(df)

    df = saving_csv(df)

    return df