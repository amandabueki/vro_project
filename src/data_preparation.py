"""
data_preparation.py

Functions for loading and preparing the precipitation and temperature dataset for the 
analysis of the relationship between heavy rainfall events and climate change.
"""

from pathlib import Path
import pandas as pd

# ================================================================================
# Daily data
# ================================================================================

# Path to the processed daily dataset

PATH_DAILY = Path("data") / "processed" / "merged_data.csv"

# Load the merged CSV file

def load_daily_dataset(path: Path = PATH_DAILY) -> pd.DataFrame:

    print("Loading dataset...")
    df = pd.read_csv(path)
    print(f"Daily dataset loaded successfully ({len(df)} rows).")

    return df

# The three columns we need from the original daily dataset; date, precipitation amount and temperature

def select_columns(df: pd.DataFrame) -> pd.DataFrame:

    columns = ["date",
               "regional_mean_precip_mm",
               "regional_mean_temperature_degC"]

    return df[columns].copy()

# Changing the column names for easy usage during the project

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:

    return df.rename(columns={"regional_mean_precip_mm": "rain_mm",
                              "regional_mean_temperature_degC": "temp_C"})

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
    df["season"] = ((df["month"] % 12) // 3 + 1).astype(int)

    return df

# Saving new csv with columns needed for further analysis

def saving_csv(df: pd.DataFrame) -> pd.DataFrame:

    df.to_csv("data/processed/weather_data.csv", index=False)

    return df

# ================================================================================
# Pipeline funtion
# ================================================================================

def prepare_dataset() -> pd.DataFrame:

    df = load_daily_dataset()

    df = select_columns(df)

    df = rename_columns(df)

    df = convert_date(df)

    df = create_time_features(df)

    df = saving_csv(df)

    return df