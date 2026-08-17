"""
evaluation.py

Functions for evaluating the relationship between precipitation and temperature indicators.
"""

import pandas as pd
from scipy.stats import pearsonr

# correlation function

def calculate_correlation(df: pd.DataFrame,
                          x_column: str,
                          y_column: str):

    correlation, p_value = pearsonr(df[x_column], df[y_column])

    print(f"Correlation: {correlation:.3f}")
    print(f"P-value: {p_value:.5f}")

    return correlation, p_value

# comparison of annual mean temperature and annual maximum rainfall

def compare_temp_max_precip(
        annual_temp: pd.DataFrame,
        annual_max_precip: pd.DataFrame):

    comparison = pd.merge(
        annual_temp,
        annual_max_precip,
        on="year"
    )

    correlation, p_value = pearsonr( 
        comparison["mean_temp_C"], 
        comparison["max_precip_mm"] ) 

    print(f"Pearson correlation: {correlation:.3f}") 
    print(f"P-value: {p_value:.5f}") 

    return comparison, correlation, p_value
    
# comparison of annual mean temperature and the number of heavy rainfall days

def compare_temp_heavy_rainfall(
        annual_temp: pd.DataFrame,
        heavy_rain_days: pd.DataFrame):

    comparison = pd.merge(
        annual_temp,
        heavy_rain_days,
        on="year",
        how="left"
    )

    comparison["heavy_rain_days"] = (
        comparison["heavy_rain_days"]
        .fillna(0)
        .astype(int)
    )

    correlation, p_value = calculate_correlation(
        comparison,
        "mean_temp_C",
        "heavy_rain_days"
    )

    return comparison, correlation, p_value

# comparison of monthly and seasonal temperature and seasonal heavy rainfall frequency

def compare_monthly_temp_heavy_rainfall(
        monthly_temp: pd.DataFrame,
        monthly_rain_days: pd.DataFrame):

    comparison = pd.merge(
        monthly_temp,
        monthly_rain_days,
        on="month",
        how="left"
    )

    comparison["heavy_rain_days"] = (
        comparison["heavy_rain_days"]
        .fillna(0)
        .astype(int)
    )

    correlation, p_value = calculate_correlation(
        comparison,
        "mean_temp_C",
        "heavy_rain_days"
    )

    return comparison, correlation, p_value

def compare_seasonal_temp_heavy_rainfall(
        seasonal_temp: pd.DataFrame,
        seasonal_rain_days: pd.DataFrame):

    comparison = pd.merge(
        seasonal_temp,
        seasonal_rain_days,
        on="season",
        how="left"
    )

    comparison["heavy_rain_days"] = (
        comparison["heavy_rain_days"]
        .fillna(0)
        .astype(int)
    )

    correlation, p_value = calculate_correlation(
        comparison,
        "mean_temp_C",
        "heavy_rain_days"
    )

    return comparison, correlation, p_value

# comparison of annual mean temperature and days above the 95th percentile

def compare_temp_percentile_days(
        annual_temp: pd.DataFrame,
        percentile_days: pd.DataFrame,
        percentile: int = 95):

    comparison = pd.merge(
        annual_temp,
        percentile_days,
        on="year",
    )

    correlation, p_value = pearsonr(
        comparison["mean_temp_C"],
        comparison["percentile_days"]
    )

    print(
        f"Pearson correlation (Temperature vs Days above {percentile}th percentile): "
        f"{correlation:.3f}"
    )
    print(f"P-value: {p_value:.5f}")

    return comparison, correlation, p_value