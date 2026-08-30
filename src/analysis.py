"""
analysis.py

Functions for analysing long-term precipitation and temperature data to investigate 
the relationship between heavy rainfall events and climate change.
"""

import pandas as pd
import numpy as np
from scipy.stats import linregress

# ================================================================================
# Precipitation analysis
# ================================================================================

# annual maximum daily precipitation

def annual_max_precip(df: pd.DataFrame) -> pd.DataFrame:

    result = (
        df.groupby("year")["rain_mm"]
        .max()
        .reset_index(name="max_precip_mm")
    )

    return result

# number of days above 20 mm/day rainfall

def days_above_20mm_threshold(
        df: pd.DataFrame,
        threshold: float = 20
) -> pd.DataFrame:

    result =(
        df[df["rain_mm"] >= threshold]
        .groupby("year")
        .size()
        .reset_index(name="heavy_rain_days_20")
    )

    all_years = pd.DataFrame({
        "year": sorted(df["year"].dropna().unique())
    })
    
    result = all_years.merge(
            result,
            on="year",
            how="left"
        )
            
    result["heavy_rain_days_20"] = (
            result["heavy_rain_days_20"]
            .fillna(0)
            . astype(int)
        )
    
    return result

# number of days above 30 mm/day rainfall

def days_above_30mm_threshold(
    df: pd.DataFrame,
    threshold: float = 30
) -> pd.DataFrame:

    result =(
        df[df["rain_mm"] >= threshold]
        .groupby("year")
        .size()
        .reset_index(name="heavy_rain_days_30")
    )

    all_years = pd.DataFrame({
        "year": sorted(df["year"].dropna().unique())
    })

    result = all_years.merge(
        result,
        on="year",
        how="left"
    )
        
    result["heavy_rain_days_30"] = (
        result["heavy_rain_days_30"]
        .fillna(0)
        . astype(int)
    )

    return result

# number of days above 40 mm/day rainfall

def days_above_40mm_threshold(
    df: pd.DataFrame,
    threshold: float = 40
) -> pd.DataFrame:

    result =(
        df[df["rain_mm"] >= threshold]
        .groupby("year")
        .size()
        .reset_index(name="heavy_rain_days_40")
    )

    all_years = pd.DataFrame({
        "year": sorted(df["year"].dropna().unique())
    })

    result = all_years.merge(
        result,
        on="year",
        how="left"
    )
        
    result["heavy_rain_days_40"] = (
        result["heavy_rain_days_40"]
        .fillna(0)
        . astype(int)
    )

    return result

# number of days above the 95th percentile

def precip_percentile(
    df: pd.DataFrame,
    percentile: int = 95
) -> float:

    values = df["rain_mm"].dropna()

    if values.empty:
        return np.nan

    return float(
        np.percentile(values, percentile)
    )

# number of days above the 99th percentile

def days_above_percentile(
    df: pd.DataFrame,
    percentile: int = 99
) -> pd.DataFrame:

    threshold = precip_percentile(df, percentile)

    column = f"days_above_{percentile}th_percentile"

    result = (
        df[df["rain_mm"] >= threshold]
        .groupby("year")
        .size()
        .reset_index(name=column)
    )

    all_years = pd.DataFrame({
        "year": sorted(df["year"].dropna().unique())
    })

    result = all_years.merge(
        result,
        on="year",
        how="left"
    )

    result [column] = (
        result[column]
        .fillna(0)
        .astype(int)
    )

    return result

# maximum precipitation over three & five consecutive days

def max_consecutive_precip(
    df: pd.DataFrame,
    window: int
) -> pd.DataFrame:

    df = df.sort_values("date").copy()

    results = []

    for year, group in df.groupby("year"):
        group = group.sort_values("date")
        rolling_sum = (
            group["rain_mm"]
            .rolling(window=window, min_periods=window)
            .sum()
        )

        results.append({
            "year": year,
            f"max_{window}_day_precip_mm": rolling_sum.max()
        })

    return pd.DataFrame(results)

def max_consecutive_precip_three(
    df: pd.DataFrame,
    window: int = 3
) -> pd.DataFrame:

    return max_consecutive_precip(df, window)

def max_consecutive_precip_five(
        df: pd.DataFrame,
        window: int = 5
) -> pd.DataFrame:

    return max_consecutive_precip(df, window)

# three & five consecutive days with 20 mm/day



# monthly and seasonal distribution of heavy rainfall

def monthly_precip(df: pd.DataFrame) -> pd.DataFrame:

    all_months = pd.DataFrame({
        "month": range(1, 13)
    })

    days20 = (
        df[df["rain_mm"] >= 20]
        .groupby("month")
        .size()
        .reset_index(name="heavy_rain_days_20")
    )

    days30 = (
        df[df["rain_mm"] >= 30]
        .groupby("month")
        .size()
        .reset_index(name="heavy_rain_days_30")
    )

    days40 = (
        df[df["rain_mm"] >= 40]
        .groupby("month")
        .size()
        .reset_index(name="heavy_rain_days_40")
    )

    result = all_months.merge(days20, on="month", how="left")
    result = result.merge(days30, on="month", how="left")
    result = result.merge(days40, on="month", how="left")

    result["heavy_rain_days_20"] = (
        result["heavy_rain_days_20"].fillna(0).astype(int)
    )

    result["heavy_rain_days_30"] = (
        result["heavy_rain_days_30"].fillna(0).astype(int)
    )

    result["heavy_rain_days_40"] = (
        result["heavy_rain_days_40"].fillna(0).astype(int)
    )

    return result

def seasonal_precip(df: pd.DataFrame) -> pd.DataFrame:

    years = sorted(df["year"].dropna().unique())

    all_combinations = pd.MultiIndex.from_product(
        [years, [1, 2, 3, 4]],
        names=["year", "season"]
    ).to_frame(index=False)

    days20 = (
        df[df["rain_mm"] >= 20]
        .groupby(["year", "season"])
        .size()
        .reset_index(name="heavy_rain_days_20")
    )

    days30 = (
        df[df["rain_mm"] >= 30]
        .groupby(["year", "season"])
        .size()
        .reset_index(name="heavy_rain_days_30")
        )

    days40 = (
        df[df["rain_mm"] >= 40]
        .groupby(["year", "season"])
        .size()
        .reset_index(name="heavy_rain_days_40")
    )

    result = all_combinations.merge(days20, on=["year", "season"], how="left")
    result = result.merge(days30, on=["year", "season"], how="left")
    result = result.merge(days40, on=["year", "season"], how="left")

    result["heavy_rain_days_20"] = (
        result["heavy_rain_days_20"].fillna(0).astype(int)
    )

    result["heavy_rain_days_30"] = (
        result["heavy_rain_days_30"].fillna(0).astype(int)
    )

    result["heavy_rain_days_40"] = (
        result["heavy_rain_days_40"].fillna(0).astype(int)
    )

    return result

# Seasonal heavy rainfall frequency (20 mm/day & 30 mm/day)

def seasonal_heavy_rainfall_summary(seasonal_data: pd.DataFrame):

    return(
        seasonal_data
        .groupby("season", as_index=False)
        [
            [
                "heavy_rain_days_20",
                "heavy_rain_days_30"
            ]
        ]
        .mean()
    )

# calculation of seasonal percentile days

def seasonal_percentile_days(
        df: pd.DataFrame,
        percentile: int
) -> pd.DataFrame:

    threshold = precip_percentile(df, percentile)

    column = f"days_above_{percentile}th_percentile"

    result = (
        df[df["rain_mm"] >= threshold]
        .groupby(["year", "season"])
        .size()
        .reset_index(name=column)
    )

    return result

# ================================================================================
# Analysis of temperature
# ================================================================================

# anual & seasonal mean temperature

def annual_mean_temp(df: pd.DataFrame) -> pd.DataFrame:

    return (
        df
        .groupby("year", as_index=False)["temp_C"]
        .mean()
        .rename(
            columns={
                "temp_C": "mean_temp_C"
            }
        )
    )

# Seasonal mean temperature

def seasonal_mean_temp(df: pd.DataFrame) -> pd.DataFrame:

    return (
        df
        .groupby(
            ["year", "season"],
            as_index=False
        )["temp_C"]
        .mean()
        .rename(
            columns={
                "temp_C": "mean_temp_C"
            }
        )
    )

# monthly mean temperature

def monthly_mean_temp(df: pd.DataFrame) -> pd.DataFrame:

    return (
        df
        .groupby(
            "month",
            as_index=False
        )["temp_C"]
        .mean()
        .rename(
            columns={
                "temp_C": "mean_temp_C"
            }
        )
    )

# temperature anomalies

def temp_anomalies(df: pd.DataFrame) -> pd.DataFrame:

    annual = annual_mean_temp(df)

    reference_mean = annual["mean_temp_C"].mean()

    annual["temp_anomaly_C"] = (
        annual["mean_temp_C"]
        - reference_mean
    )

    return annual

# long term temperature trend

def temp_trend(df: pd.DataFrame) -> dict:

    annual = annual_mean_temp(df).dropna()

    if len(annual) < 2:
        return {
            "slope_C_per_year": np.nan,
            "intercept": np.nan,
            "r_value": np.nan,
            "p_value": np.nan,
            "r_squared": np.nan
        }

    regression = linregress(
        annual["year"],
        annual["mean_temp_C"]
    )

    return {
        "slope_C_per_year": regression.slope,
        "intercept": regression.intercept,
        "r_value": regression.rvalue,
        "p_value": regression.pvalue,
        "r_squared": regression.rvalue ** 2
    }