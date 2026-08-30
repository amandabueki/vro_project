"""
correlation.py

Functions for calculating the correlation between precipitation and temperature indicators.
"""

import numpy as np
import pandas as pd
from scipy.stats import linregress

# general correlation function

def calculate_correlation(
    df: pd.DataFrame,
    x_column: str,
    y_column: str
):
    if x_column not in df.columns or y_column not in df.columns:
        return {
            "x_variable": x_column,
            "y_variable": y_column,
            "correlation": np.nan,
            "p_value": np.nan,
            "slope": np.nan,
            "n": 0
        }

    data = df[
        [x_column, y_column]
    ].dropna()

    if len(data) < 2:
        return {
            "x_variable": x_column,
            "y_variable": y_column,
            "correlation": np.nan,
            "p_value": np.nan,
            "slope": np.nan,
            "n": len(data)
        }

    if (
        data[x_column].nunique() < 2
        or data[y_column].nunique() < 2
    ):
        return {
            "x_variable": x_column,
            "y_variable": y_column,
            "correlation": np.nan,
            "p_value": np.nan,
            "slope": np.nan,
            "n": len(data)
        }

    result = linregress(
        data[x_column],
        data[y_column]
    )

    return {
        "x_variable": x_column,
        "y_variable": y_column,
        "correlation": result.rvalue,
        "p_value": result.pvalue,
        "slope": result.slope,
        "n": len(data)
    }

# ================================================================================
# Annual comparisons
# ================================================================================

# comparison of annual mean temperature and annual maximum rainfall

def compare_temp_max_precip(annual_data: pd.DataFrame):

    return calculate_correlation(
        annual_data,
        "mean_temp_C",
        "max_precip_mm"
    )

# temperature vs. heavy rainfall days (≥ 20 mm/day & ≥ 30 mm/day)
# comparison of annual mean temperature and the number of heavy rainfall days 

def compare_temp_heavy_rainfall(annual_data: pd.DataFrame):

    results = []

    for threshold in [20, 30]:
        column = f"heavy_rain_days_{threshold}"

        result = calculate_correlation(
            annual_data,
            "mean_temp_C",
            column
        )

        result["threshold_mm"] = threshold

        results.append(result)

    return pd.DataFrame(results)

# comparison of annual mean temperature and days above the 95th & 99th percentile

def compare_temp_percentile_days(annual_data: pd.DataFrame):

    results = []

    percentile_columns = {
        95: "days_above_95th_percentile",
        99: "days_above_99th_percentile"
    }

    for percentile, column in percentile_columns.items():

        result = calculate_correlation(
            annual_data,
            "mean_temp_C",
            column
        )

        result["percentile"] = percentile

        results.append(result)

    return pd.DataFrame(results)

# ================================================================================
# Seasonal relationships
# ================================================================================

# comparison of seasonal temperature and heavy rainfall

def seasonal_temperature_vs_heavy_rainfall(seasonal_data: pd.DataFrame):

    results = []

    for season in [1, 2, 3, 4]:

        season_data = seasonal_data[
            seasonal_data["season"] == season
        ]

        for threshold in [20, 30]:
            rainfall_column = f"heavy_rain_days_{threshold}"

            result = calculate_correlation(
                season_data,
                "mean_temp_C",
                rainfall_column
            )

            result["season"] = season
            result["threshold_mm"] = threshold

            results.append(result)

    return pd.DataFrame(results)

# comparison of seasonal temperature and percentile days

def seasonal_temperature_vs_percentile_days(seasonal_data:pd.DataFrame):

    results = []

    percentile_columns = {
        95: "days_above_95th_percentile",
        99: "days_above_99th_percentile"
    }

    for season in [1, 2, 3, 4]:
        season_data = seasonal_data[
            seasonal_data["season"] == season
        ]

        for percentile, column in percentile_columns.items():
            if column not in season_data.columns:
                continue

            result = calculate_correlation(
                season_data,
                "mean_temp_C",
                column
            )

            result["season"] = season
            result["percentile"] = percentile

            results.append(result)

    return pd.DataFrame(results)

# ================================================================================
# Monthly relationsships
# ================================================================================

# comparison of monthly temperature and heavy rainfall

def monthly_temperature_vs_heavy_rainfall(monthly_data: pd.DataFrame):

    results = []

    for month in sorted(monthly_data["month"].unique()):

        month_data = monthly_data[
            monthly_data["month"] == month
        ]

        for threshold in [20, 30]:
            rainfall_column = f"heavy_rain_days_{threshold}"

            result = calculate_correlation(
                month_data,
                "mean_temp_C",
                rainfall_column
            )

            result["month"] = month
            result["threshold_mm"] = threshold

            results.append(result)

    return pd.DataFrame(results)


# ================================================================================
# Earlier vs. recent periods
# ================================================================================

# comparison of precipitation periods

def compare_precipitation_periods(
        annual_data: pd.DataFrame,
        earlier_start: int,
        earlier_end:int,
        recent_start: int,
        recent_end: int
) -> pd.DataFrame:

    earlier = annual_data[
        (annual_data["year"] >= earlier_start) &
        (annual_data["year"] <= earlier_end)
    ]

    recent = annual_data[
        (annual_data["year"] >= recent_start) &
        (annual_data["year"] <= recent_end)
    ]

    return pd.DataFrame({
        "period": [
            f"{earlier_start}-{earlier_end}",
            f"{recent_start}-{recent_end}"
        ],
        "mean_max_precip_mm": [
            earlier["max_precip_mm"].mean(),
            recent["max_precip_mm"].mean()
        ],
        "mean_heavy_rain_days_20": [
            earlier["heavy_rain_days_20"].mean(),
            recent["heavy_rain_days_20"].mean()
        ],
        "mean_heavy_rain_days_30": [
            earlier["heavy_rain_days_30"].mean(),
            recent["heavy_rain_days_30"].mean()
        ]
    })

# comparison of temperature

def compare_temperature_periods(
        annual_data: pd.DataFrame,
        earlier_start: int,
        earlier_end: int,
        recent_start: int,
        recent_end: int
) -> pd.DataFrame:

    earlier = annual_data[
        (annual_data["year"] >= earlier_start) &
        (annual_data["year"] <= earlier_end)
    ]

    recent = annual_data[
        (annual_data["year"] >= recent_start) &
        (annual_data["year"] <= recent_end)
    ]

    return pd.DataFrame({
        "period": [
            f"{earlier_start}-{earlier_end}",
            f"{recent_start}-{recent_end}"
        ],
        "mean_temp_C": [
            earlier["mean_temp_C"].mean(),
            recent["mean_temp_C"].mean()
        ]
    })

# ================================================================================
# Combined evaluation
# ================================================================================

def run_evaluation(
        annual_data: pd.DataFrame,
        seasonal_data: pd.DataFrame
):
    results = {}

    results["annual_temp_vs_max_precip"] = (
        compare_temp_max_precip(annual_data)
    )

    results["annual_temp_vs_heavy_rainfall"] = (
        compare_temp_heavy_rainfall(annual_data)
    )

    results["annual_temp_vs_percentile_days"] = (
        compare_temp_percentile_days(annual_data)
    )

    results["seasonal_temp_vs_heavy_rainfall"] = (
        seasonal_temperature_vs_heavy_rainfall(seasonal_data)
    )

    results["seasonal_temp_vs_percentile_days"] = (
        seasonal_temperature_vs_percentile_days(seasonal_data)
    )

    return results