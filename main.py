"""
main.py

Main script for the heavy rainfall analysis.
"""

import pandas as pd

from src.data_preparation import prepare_dataset

from src.analysis import (
    annual_max_precip,
    days_above_20mm_threshold,
    days_above_30mm_threshold,
    days_above_40mm_threshold,
    precip_percentile,
    days_above_percentile,
    max_consecutive_precip,
    max_consecutive_precip_three,
    max_consecutive_precip_five,
    monthly_precip,
    seasonal_precip,
    seasonal_heavy_rainfall_summary,
    seasonal_percentile_days,
    annual_mean_temp,
    seasonal_mean_temp,
    monthly_mean_temp,
    temp_anomalies,
    temp_trend
)

from src.visualization import (
    plot_annual_mean_temp,
    plot_seasonal_mean_temp_years,
    plot_monthly_mean_temp,
    plot_temp_trend,
    plot_annual_max_precip,
    plot_heavy_rainfall_days,
    plot_percentile_days,
    plot_monthly_dist,
    plot_seasonal_dist,
    plot_max_consecutive_precip,
    plot_temp_vs_max_precip,
    plot_temp_vs_heavy_rainfall,
    plot_temp_vs_percentile,
    plot_monthly_temp_vs_rain,
    plot_seasonal_temp_vs_rain
)

from src.correlation import (
    calculate_correlation,
    compare_temp_max_precip,
    compare_temp_heavy_rainfall,
    compare_temp_percentile_days,
    seasonal_temperature_vs_heavy_rainfall,
    seasonal_temperature_vs_percentile_days,
    monthly_temperature_vs_heavy_rainfall,
    compare_precipitation_periods,
    compare_temperature_periods
)

def main():
    # Preparing the dataset
    df = prepare_dataset()

    # Precipitation analysis
    annual_max = annual_max_precip(df)
    days20 = days_above_20mm_threshold(df,20)
    days30 = days_above_30mm_threshold(df,30)
    days40 = days_above_40mm_threshold(df,40)
    days95 = days_above_percentile(df,95)
    days99 = days_above_percentile(df,99)
    monthly = monthly_precip(df)
    seasonal = seasonal_precip(df)
    max3 = max_consecutive_precip_three(df,3)
    max5 = max_consecutive_precip_five(df,5)

    # Temperature analysis
    annual_temp = annual_mean_temp(df)
    seasonal_temp = seasonal_mean_temp(df)
    monthly_temp = monthly_mean_temp(df)
    trend = temp_trend(df)

    # Creating annual evaluation dataset
    annual_data = annual_temp.merge(
        annual_max,
        on="year",
        how="outer"
    )
    annual_data = annual_data.merge(
        days20,
        on="year",
        how="outer"
    )
    annual_data = annual_data.merge(
        days30,
        on="year",
        how="outer"
    )
    annual_data = annual_data.merge(
        days40,
        on="year",
        how="outer"
    )
    annual_data = annual_data.merge(
        days95,
        on="year",
        how="outer"
    )
    annual_data = annual_data.merge(
        days99,
        on="year",
        how="outer"
    )

    # Creating seasonal evaluation dataset
    seasonal_data = seasonal_temp.merge(
        seasonal,
        on=["year", "season"],
        how="outer"
    )

    for percentile in [95, 99]:

        seasonal_percentile = seasonal_percentile_days(
            df,
            percentile
        )

        seasonal_data = seasonal_data.merge(
            seasonal_percentile,
            on=["year", "season"],
            how="left"
        )

        column= f"days_above_{percentile}th_percentile"

        seasonal_data[column] = (
            seasonal_data[column]
            .fillna(0)
            .astype(int)
        )

    # Creating monthly evaluation dataset
    monthly_data = monthly_temp.merge(
        monthly,
        on="month",
        how="outer"
    )

    # Period comparison 
    earlier_start = 1950
    earlier_end = 1959

    recent_start = 2016
    recent_end = 2025

    precip_period_comparison = compare_precipitation_periods(
        annual_data,
        earlier_start=earlier_start,
        earlier_end=earlier_end,
        recent_start=recent_start,
        recent_end=recent_end
    )

    temp_period_comparison = compare_temperature_periods(
        annual_data,
        earlier_start=earlier_start,
        earlier_end=earlier_end,
        recent_start=recent_start,
        recent_end=recent_end
    )

    print("\nPrecipitation period comparison:")
    print(precip_period_comparison)

    print("\nTemperature period comparison:")
    print(temp_period_comparison)

    # Statistical relationsships

    print("\nAnnual temperature vs. maximum precipitation:")
    print(
        compare_temp_max_precip(annual_data)
    )

    print("\nAnnual temperature vs. heavy rainfall:")
    print(
        compare_temp_heavy_rainfall(annual_data)
    )

    print("\nAnnual temperature vs. percentile days:")
    print(
        compare_temp_percentile_days(annual_data)
    )

    print("\nSeasonal temperature summary:")
    print(
    pd.concat([
        seasonal_temp.head(12),
        seasonal_temp.tail(12)
    ])
)

    print("\nSeasonal heavy rainfall summary:")
    print(
        seasonal_heavy_rainfall_summary(seasonal_data)
    )

    print("\nSeasonal temperature vs. heavy rainfall:")
    print(
        seasonal_temperature_vs_heavy_rainfall(seasonal_data)
    )

    print("\nSeasonal temperature vs. percentile days:")
    print(
        seasonal_temperature_vs_percentile_days(seasonal_data)
    )

    # Visualization
    plot_annual_mean_temp(annual_temp)
    plot_seasonal_mean_temp_years(seasonal_temp)
    plot_temp_trend(annual_temp, trend)
    plot_annual_max_precip(annual_max)
    plot_heavy_rainfall_days(days20,days30,days40)
    plot_percentile_days(days95, days99)
    plot_max_consecutive_precip(max3, max5)
    plot_monthly_dist(monthly)
    plot_monthly_mean_temp(monthly_temp)
    plot_seasonal_dist(seasonal)
    plot_temp_vs_max_precip(annual_data)
    plot_temp_vs_heavy_rainfall(annual_data, threshold=20)
    plot_temp_vs_heavy_rainfall(annual_data, threshold=30)
    plot_temp_vs_heavy_rainfall(annual_data, threshold=40)
    plot_temp_vs_percentile(annual_data, percentile=95)
    plot_temp_vs_percentile(annual_data, percentile=99)
    plot_monthly_temp_vs_rain(monthly_data)
    plot_seasonal_temp_vs_rain(seasonal_data, threshold=20)
    plot_seasonal_temp_vs_rain(seasonal_data, threshold=30)
    plot_seasonal_temp_vs_rain(seasonal_data, threshold=40)

    print("\nAnalysis completed successfully.")

# Running program

if __name__ == "__main__":
    main()