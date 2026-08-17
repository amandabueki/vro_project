"""
analysis.py

Functions for analysing long-term precipitation and temperature data to investigate 
the relationship between heavy rainfall events and climate change.
"""

import pandas as pd
import numpy as np
from scipy.stats import linregress

# ================================================================================
# Analysis of precipitation
# ================================================================================

# maximum daily precipitation in each year

def annual_max_precip(df: pd.DataFrame) -> pd.DataFrame:

    result = (
        df.groupby("year")["rain_mm"]
        .max()
        .reset_index(name="max_precip_mm")
    )

    return result

# number of days above 15 mm in 1 hour rainfall (heavy rainfall events)

def days_above_15mm_threshold(
        df: pd.DataFrame,
        threshold: float = 15
) -> pd.DataFrame:

    result =(
        df[df["rain_1_mm/h"] >= threshold]
        .groupby("year")
        .size()
        .reset_index(name="heavy_rain_days")
    )

     # add years with no days above threshold
    all_years = pd.DataFrame({"year": sorted(df["year"].unique())})
    
    result = pd.merge(
            all_years,
            result,
            on="year",
            how="left"
        )
            
    result["heavy_rain_days"] = (
            result["heavy_rain_days"]
            .fillna(0)
            . astype(int)
        )
    
    return result

# number of days above 20 mm in 6 hours rainfall (heavy rainfall events)

def days_above_20mm_threshold(
    df: pd.DataFrame,
    threshold: float = 20
) -> pd.DataFrame:

    result =(
        df[df["rain_6_mm/h"] >= threshold]
        .groupby("year")
        .size()
        .reset_index(name="heavy_rain_days")
    )

    # add years with no days above threshold
    all_years = pd.DataFrame({"year": sorted(df["year"].unique())})

    result = pd.merge(
        all_years,
        result,
        on="year",
        how="left"
    )
        
    result["heavy_rain_days"] = (
        result["heavy_rain_days"]
        .fillna(0)
        . astype(int)
    )

    return result

# number of days above 25 mm in 1 hour rainfall (intense heavy rainfall events)

def days_above_25mm_threshold(
        df: pd.DataFrame,
        threshold: float = 25
) -> pd.DataFrame:

    result =(
        df[df["rain_1_mm/h"] >= threshold]
        .groupby("year")
        .size()
        .reset_index(name="heavy_rain_days")
    )

     # add years with no days above threshold
    all_years = pd.DataFrame({"year": sorted(df["year"].unique())})
    
    result = pd.merge(
            all_years,
            result,
            on="year",
            how="left"
        )
            
    result["heavy_rain_days"] = (
            result["heavy_rain_days"]
            .fillna(0)
            . astype(int)
        )
    
    return result

# number of days above 35 mm in 6 hour rainfall (intense heavy rainfall events)

def days_above_35mm_threshold(
    df: pd.DataFrame,
    threshold: float = 35
) -> pd.DataFrame:
    
    result =(
        df[df["rain_6_mm/h"] >= threshold]
        .groupby("year")
        .size()
        .reset_index(name="heavy_rain_days")
    )

    # add years with no days above threshold
    all_years = pd.DataFrame({"year": sorted(df["year"].unique())})

    result = pd.merge(
        all_years,
        result,
        on="year",
        how="left"
    )

    result["heavy_rain_days"] = (
        result["heavy_rain_days"]
        .fillna(0)
        . astype(int)
    )

    return result

# number of days above 40 mm in 1 hour rainfall (extrem intense heavy rainfall events)

def days_above_40mm_threshold(
        df: pd.DataFrame,
        threshold: float = 40
) -> pd.DataFrame:

    result =(
        df[df["rain_1_mm/h"] >= threshold]
        .groupby("year")
        .size()
        .reset_index(name="heavy_rain_days")
    )

     # add years with no days above threshold
    all_years = pd.DataFrame({"year": sorted(df["year"].unique())})
    
    result = pd.merge(
            all_years,
            result,
            on="year",
            how="left"
        )
            
    result["heavy_rain_days"] = (
            result["heavy_rain_days"]
            .fillna(0)
            . astype(int)
        )
    
    return result

# number of days above 60 mm in 6 hours rainfall (extrem intense heavy rainfall events)

def days_above_60mm_threshold(
    df: pd.DataFrame,
    threshold: float = 60
) -> pd.DataFrame:

    result =(
        df[df["rain_6_mm/h"] >= threshold]
        .groupby("year")
        .size()
        .reset_index(name="heavy_rain_days")
    )

    # add years with no days above threshold
    all_years = pd.DataFrame({"year": sorted(df["year"].unique())})

    result = pd.merge(
        all_years,
        result,
        on="year",
        how="left"
    )

    result["heavy_rain_days"] = (
        result["heavy_rain_days"]
        .fillna(0)
        . astype(int)
    )

    return result

# number of days above the 95th percentile

def precip_percentile(
    df: pd.DataFrame,
    percentile: int = 95
) -> float:

    return float(
        np.percentile(
            df["rain_mm"].dropna(),
            percentile
        )
    )

# number of days above the 99th percentile

def days_above_percentile(
    df: pd.DataFrame,
    percentile: int = 99
) -> pd.DataFrame:

    threshold = precip_percentile(df, percentile)

    result = (
        df[df["rain_mm"] >= threshold]
        .groupby("year")
        .size()
        .reset_index(name="percentile_days")
    )

    all_years = pd.DataFrame({"year": sorted(df["year"].unique())})

    result = pd.merge(
        all_years,
        result,
        on="year",
        how="left"
    )

    result ["percentile_days"] = (
        result["percentile_days"]
        .fillna(0)
        .astype(int)
    )

    return result

# maximum precipitation over three or five consecutive days

def max_consecutive_precip_three(
    df: pd.DataFrame,
    window: int = 3
) -> pd.DataFrame:

    df = df.sort_values("date").copy()

    result = []

    for year, group in df.groupby("year"):
        group = group.sort_values("date")
        rolling_sum = (
            group["rain_mm"]
            .rolling(window=window)
            .sum()
        )

        result.append({
            "year": year,
            f"max_{window}_day_precip_mm": rolling_sum.max()
        })

    return pd.DataFrame(result)

def max_consecutive_precip_five(
    df: pd.DataFrame,
    window: int = 5
) -> pd.DataFrame:

    df = df.sort_values("date").copy()

    result = []

    for year, group in df.groupby("year"):
        group = group.sort_values("date")
        rolling_sum = (
            group["rain_mm"]
            .rolling(window=window)
            .sum()
        )

        result.append({
            "year": year,
            f"max_{window}_day_precip_mm": rolling_sum.max()
        })

    return pd.DataFrame(result)

# monthly and seasonal distribution of heavy rainfall

def monthly_precip(df: pd.DataFrame) -> pd.DataFrame:

    result = (
        df[df["rain_mm"] >= 35]
        .groupby("month")
        .size()
        .reset_index(name="heavy_rain_days")
    )

    all_months = pd.DataFrame({
        "month": range(1, 13)
    })

    result = pd.merge(
        all_months,
        result,
        on="month",
        how="left"
    )

    result["heavy_rain_days"] = (
        result["heavy_rain_days"]
        .fillna(0)
        .astype(int)
    )

    return result

def seasonal_precip(df: pd.DataFrame) -> pd.DataFrame:

    result = (
        df[df["rain_mm"] >= 35]
        .groupby("season")
        .size()
        .reset_index(name="heavy_rain_days")
    )
    return result

# comparison of earlier and recent periods

def compare_precip_periods(
    df: pd.DataFrame,
    start_period1: int,
    end_period1: int,
    start_period2: int,
    end_period2: int
) -> pd.DataFrame:

    period1 = df[
        (df["year"] >= start_period1) &
        (df["year"] <= end_period1)
    ]

    period2 = df[
        (df["year"] >= start_period2) &
        (df["year"] <= end_period2)
    ]

    result = pd.DataFrame({
        "period": [
            f"{start_period1}-{end_period1}",
            f"{start_period2}-{end_period2}"
        ],
        "mean_daily_precip_mm": [
            period1["rain_mm"].mean(),
            period2["rain_mm"].mean()
        ],
        "max_daily_precip_mm": [
            period1["rain_mm"].max(),
            period2["rain_mm"].max()
        ],
        "days_above_35_mm": [
            (period1["rain_mm"] >= 35).sum(),
            (period2["rain_mm"] >= 35).sum()
        ]
    })

    return result

# ================================================================================
# Analysis of temperature
# ================================================================================

# anual & seasonal mean temperature

def annual_mean_temp(df: pd.DataFrame) -> pd.DataFrame:

    result = (
        df.groupby("year")["temp_C"]
        .mean()
        .reset_index(name="mean_temp_C")
    )

    return result

def seasonal_mean_temp(df: pd.DataFrame) -> pd.DataFrame:

    result = (
        df.groupby(["year","season"])["temp_C"]
        .mean()
        .reset_index(name="mean_temp_C")
    )

    return result

# monthly mean temperature

def monthly_mean_temp(df: pd.DataFrame) -> pd.DataFrame:

    result = (
        df.groupby("month")["temp_C"]
        .mean()
        .reset_index(name="mean_temp_C")
    )

    return result

# temperature anomalies

def temp_anomalies(
    df: pd.DataFrame,
    reference_start: int,
    reference_end: int
) -> pd.DataFrame:

    reference = df[
        (df["year"] >= reference_start) &
        (df["year"] <= reference_end)
    ]

    reference_mean = reference["temp_C"].mean()

    annual_temp = annual_mean_temp(df)

    annual_temp["temp_anomaly_C"] = (
        annual_temp["mean_temp_C"]
        - reference_mean
    )

    return annual_temp

# long term temperature trend

def temp_trend(df: pd.DataFrame) -> dict:

    annual_temp = annual_mean_temp(df)

    regression = linregress(
        annual_temp["year"],
        annual_temp["mean_temp_C"]
    )

    return {
        "slope_C_per_year": regression.slope,
        "intercept": regression.intercept,
        "r_value": regression.rvalue,
        "p_value": regression.pvalue,
        "r_squared": regression.rvalue ** 2
    }

# comparison of earlier and recent periods

def compare_temp_periods(
    df: pd.DataFrame,
    start_period1: int,
    end_period1: int,
    start_period2: int,
    end_period2: int
) -> pd.DataFrame:

    period1 = df[
        (df["year"] >= start_period1) &
        (df["year"] <= end_period1)
    ]

    period2 = df[
        (df["year"] >= start_period2) &
        (df["year"] <= end_period2)
    ]

    result = pd.DataFrame({
        "period": [
            f"{start_period1}-{end_period1}",
            f"{start_period2}-{end_period2}"
        ],
        "mean_temp_C": [
            period1["temp_C"].mean(),
            period2["temp_C"].mean()
        ]
    })

    return result