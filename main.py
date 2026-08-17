"""
main.py

Main script for the heavy rainfall analysis.
"""

import pandas as pd

from src.data_preparation import prepare_dataset

from src.analysis import (
    annual_max_precip,
    days_above_15mm_threshold,
    days_above_20mm_threshold,
    days_above_25mm_threshold,
    days_above_35mm_threshold,
    days_above_40mm_threshold,
    days_above_60mm_threshold,
    precip_percentile,
    days_above_percentile,
    max_consecutive_precip_three,
    max_consecutive_precip_five,
    monthly_precip,
    seasonal_precip,
    compare_precip_periods,
    annual_mean_temp,
    seasonal_mean_temp,
    monthly_mean_temp,
    temp_anomalies,
    temp_trend,
    compare_temp_periods)

from src.visualization import (
    plot_annual_mean_temp,
    plot_seasonal_mean_temp,
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
    plot_seasonal_temp_vs_rain)

from src.evaluation import (
    calculate_correlation,
    compare_temp_max_precip,
    compare_temp_heavy_rainfall,
    compare_monthly_temp_heavy_rainfall,
    compare_seasonal_temp_heavy_rainfall,
    compare_temp_percentile_days)

def main():
    # Preparing the dataset
    df = prepare_dataset()

    # Temperature analysis
    annual_temp = annual_mean_temp(df)
    seasonal_temp = seasonal_mean_temp(df)
    monthly_temp = monthly_mean_temp(df)
    trend = temp_trend(df)

    # Precipitation analysis
    annual_max = annual_max_precip(df)
    days15 = days_above_15mm_threshold(df,15)
    days20 = days_above_20mm_threshold(df,20)
    days25 = days_above_25mm_threshold(df,25)
    days35 = days_above_35mm_threshold(df,35)
    days40 = days_above_40mm_threshold(df,40)
    days60 = days_above_60mm_threshold(df,60)
    days95 = days_above_percentile(df,95)
    days99 = days_above_percentile(df,99)
    monthly = monthly_precip(df)
    seasonal = seasonal_precip(df)
    max3 = max_consecutive_precip_three(df,3)
    max5 = max_consecutive_precip_five(df,5)

    # Comparison
    earlier_start = 1950
    earlier_end = 1959

    recent_start = 2016
    recent_end = 2025

    precip_perid_comparison = compare_precip_periods(
        df,
        start_period1=earlier_start,
        end_period1=earlier_end,
        start_period2=recent_start,
        end_period2=recent_end
    )

    temp_period_comparison = compare_temp_periods(
        df,
        start_period1=earlier_start,
        end_period1=earlier_end,
        start_period2=recent_start,
        end_period2=recent_end
    )

    print("\nPrecipitation period comparison:")
    print(precip_perid_comparison)

    print("\nTemperature period comparison:")
    print(temp_period_comparison)

    # Statistical relationsships

    temp_vs_max_precip, correlation_max, p_value_max = compare_temp_max_precip(
        annual_temp,
        annual_max
    )

    temp_vs_heavy_rain, correlation_heavy, p_value_heavy = compare_temp_heavy_rainfall(
        annual_temp,
        days35
    )

    seasonal_temp_vs_rain, correlation_seasonal, p_value_seasonal = compare_seasonal_temp_heavy_rainfall(
        seasonal_temp,
        seasonal
    )

    monthly_temp_vs_rain, correlation_monthly, p_value_monthly = compare_monthly_temp_heavy_rainfall(
        monthly_temp,
        monthly
    )

    temp_vs_percentile, correlation_percentile, p_value_percentile = compare_temp_percentile_days(
        annual_temp,
        days95,
        percentile=95
    )

    # Visualization
    plot_annual_mean_temp(annual_temp)
    plot_seasonal_mean_temp(seasonal_temp)
    plot_temp_trend(annual_temp, trend)
    plot_annual_max_precip(annual_max)
    plot_heavy_rainfall_days(days15,days20,days25,days35,days40,days60)
    plot_annual_max_precip(annual_max)
    plot_percentile_days(days95, days99)
    plot_max_consecutive_precip(max3, max5)
    plot_monthly_dist(monthly)
    plot_seasonal_dist(seasonal)
    plot_temp_vs_max_precip(temp_vs_max_precip)
    plot_temp_vs_heavy_rainfall(temp_vs_heavy_rain, threshold=35)
    plot_temp_vs_percentile(temp_vs_percentile, percentile=95)
    plot_monthly_temp_vs_rain(monthly_temp_vs_rain)
    plot_seasonal_temp_vs_rain(seasonal_temp_vs_rain)

    print("Analysis completed successfully.")

# Running program

if __name__ == "__main__":
    main()