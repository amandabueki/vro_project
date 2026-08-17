"""
visualization.py

Already calculated values become useful diagrams for the report.
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from scipy import stats
from pathlib import Path

# Path for saving graphs

FIGURE_DIR = Path("reports/figures")
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# ================================================================================
# Temperature
# ================================================================================

# anual mean temperature: Liniendiagramm

def plot_annual_mean_temp(annual_temp):

    plt.figure(figsize=(10, 5))

    plt.plot(
        annual_temp["year"],
        annual_temp["mean_temp_C"],
        marker="o"
    )

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.xlabel("Year")
    plt.ylabel("Mean temperature (°C)")
    plt.title("Annual mean temperature")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "annual_mean_temp.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

# seasonal mean temperature: Gruppiertes Liniendiagramm für 1950, Durchschnitt oder Mitte und 2025

def plot_seasonal_mean_temp(seasonal_temp):

    selected_years = [1950, 1975, 2000, 2025]

    plt.figure(figsize=(9, 6))

    for year in selected_years:

        year_data = seasonal_temp[
            seasonal_temp["year"] == year
        ]

        plt.plot(
            year_data["season"],
            year_data["mean_temp_C"],
            label=str(year),
            marker='o',
            ms=6
        )

    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.xticks(ticks=[1, 2, 3, 4], labels=["Winter", "Spring", "Summer", "Autumn"])
    plt.xlabel("Season")
    plt.ylabel("Mean temperature (°C)")
    plt.title("Seasonal mean temperature (°C) in selected years")
    plt.legend(title="Year")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "seasonal_mean_temp.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

# temperature trend: Streudiagramm + Trendlinie

def plot_temp_trend(annual_temp, trend):

    years = annual_temp["year"]
    temperatures = annual_temp["mean_temp_C"]

    trend_values = (
        trend["slope_C_per_year"] * years
        + trend["intercept"]
    )

    plt.figure(figsize=(10, 5))

    plt.scatter(
        years,
        temperatures,
        s=20,
        label="Linear trend"
    )

    plt.plot(
        years,
        trend_values,
        color="red",
        linestyle="-",
        linewidth=2,
        label="Trend line"
    )

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.xlabel("Year")
    plt.ylabel("Mean temperature (°C)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "temp_trend.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

# ================================================================================
# Precipitation
# ================================================================================

# whether heavy rainfall indicators changed
# maximum daily precipitation: Liniendiagramm

def plot_annual_max_precip(max_precip):

    plt.figure(figsize=(10, 5))

    plt.plot(
        max_precip["year"],
        max_precip["max_precip_mm"],
        marker="o"
    )

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.xlabel("Year")
    plt.ylabel("Maximum daily precipitation (mm)")
    plt.title("Annual maximum daily precipitation")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "annual_max_precip.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

# heavy rainfall days: Gruppiertes Liniendiagramm von 15, 20, 25, 30, 40 und 60 mm in 1 und 6 Stunden

def plot_heavy_rainfall_days(days15, days20, days25, days35, days40, days60):

    plt.figure(figsize=(10, 5))

    plt.plot(
        days15["year"],
        days15["heavy_rain_days"],
        label="number of days with ≥ 15 mm/h"
    )

    plt.plot(
        days20["year"],
        days20["heavy_rain_days"],
        label="number of days with ≥ 20 mm/6h"
    )

    plt.plot(
        days25["year"],
        days25["heavy_rain_days"],
        label="number of days with ≥ 25 mm/h"
    )

    plt.plot(
        days35["year"],
        days35["heavy_rain_days"],
        label="number of days with ≥ 35 mm/6h"
    )

    plt.plot(
        days40["year"],
        days40["heavy_rain_days"],
        label="number of days with ≥ 40 mm/h"
    )

    plt.plot(
        days60["year"],
        days60["heavy_rain_days"],
        label="number of days with ≥ 60 mm/6h"
    )

    plt.xlabel("Year")
    plt.ylabel("Number of days")
    plt.title("Annual frequency of heavy rainfall days")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "heavy_rainfall_days.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

# percentile days: Gruppiertes Liniendiagramm von 95 und 99 %

def plot_percentile_days(days95, days99):

    plt.figure(figsize=(10, 5))

    plt.plot(
        days95["year"],
        days95["percentile_days"],
        label="95th percentile"
    )

    plt.plot(
        days99["year"],
        days99["percentile_days"],
        label="99th percentile"
    )

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.xlabel("Year")
    plt.ylabel("Number of days")
    plt.title("Annual frequency of extreme precipitation days")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "percentile_days.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

# monthly distribution of heavy rainfall events: Gruppiertes Balkendiagramm

def plot_monthly_dist(monthly_dist):

    plt.figure(figsize=(10, 5))

    plt.bar(
        monthly_dist["month"],
        monthly_dist["heavy_rain_days"]
    )

    plt.xticks(ticks=[1, 2, 3, 4, 5, 6, 
                      7, 8, 9, 10, 11, 12
                      ], 
                labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
                        ]
                )
    plt.xlabel("Month")
    plt.ylabel("Number of heavy rainfall days")
    plt.title("Monthly distribution of heavy rainfall")
    plt.xticks(range(1, 13))
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "monthly_dist.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

# seasonal distribution of heavy rainfall events

def plot_seasonal_dist(seasonal_dist):

    plt.figure(figsize=(10, 5))

    plt.bar(
        seasonal_dist["season"],
        seasonal_dist["heavy_rain_days"]
    )

    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.xticks(ticks=[1, 2, 3, 4], labels=["Winter", "Spring", "Summer", "Autumn"])
    plt.xlabel("Season")
    plt.ylabel("Number of heavy rainfall days")
    plt.title("Seasonal distribution of heavy rainfall")
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "seasonal_dist.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

# maximum consecutive precipitation over 3 or 5 days

def plot_max_consecutive_precip(max3, max5):

    plt.figure(figsize=(10, 5))

    plt.plot(
        max3["year"],
        max3["max_3_day_precip_mm"],
        label="Maximum 3-day precipitation"
    )

    plt.plot(
        max5["year"],
        max5["max_5_day_precip_mm"],
        label="Maximum 5-day precipitation"
    )

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.xlabel("Year")
    plt.ylabel("Precipitation (mm)")
    plt.title("Maximum precipitation over consecutive days")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "max_consecutive_precip.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

# ================================================================================
# Relationsships
# ================================================================================

# whether temperature and rainfall indicators are statistically associated
# temperature vs. maximum rainfall: Scatterplot & Regressionslinie, r und p-Wert

def plot_temp_vs_max_precip(comparison):

    plt.figure(figsize=(10, 5))

    plt.scatter(
        comparison["mean_temp_C"],
        comparison["max_precip_mm"]
    )

    x = comparison["mean_temp_C"]
    y = comparison["max_precip_mm"]

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    plt.plot(x, slope * x + intercept, color= "red", label="Regression line")

    textstr = f"r = {r_value:.3f}\np-value = {p_value:.4e}"
    plt.gca().text(
        0.95,
        0.95,
        textstr,
        transform=plt.gca().transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.5)        
    )

    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.xlabel("Annual mean temperature (°C)")
    plt.ylabel("Annual maximum precipitation (mm)")
    plt.title("Annual mean temperature vs. annual maximum precipitation")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "temp_vs_max_precip.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

# temperature vs. heavy rainfall days: Scatterplot & Regressionslinie, r und p-Wert

def plot_temp_vs_heavy_rainfall(comparison, threshold):

    plt.figure(figsize=(10, 5))

    plt.scatter(
        comparison["mean_temp_C"],
        comparison["heavy_rain_days"]
    )

    x = comparison["mean_temp_C"]
    y = comparison["heavy_rain_days"]
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    plt.plot(x, slope * x + intercept, color= "red", label="Regression line")
    
    textstr = f"r = {r_value:.3f}\np-value = {p_value:.4e}"
    plt.gca().text(
        0.95,
        0.95,
        textstr,
        transform=plt.gca().transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.5)        
    )

    plt.xlabel("Annual mean temperature (°C)")
    plt.ylabel("Number of heavy rainfall days")
    plt.title(
        f"Annual mean temperature vs. days ≥ {threshold} mm/day"
    )
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "temp_vs_heavy_rainfall.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

# temperature vs. 95 percentile days: Scatterplot & Regressionslinie, r und p-Wert

def plot_temp_vs_percentile(comparison, percentile):

    plt.figure(figsize=(10, 5))

    plt.scatter(
        comparison["mean_temp_C"],
        comparison["percentile_days"]
    )

    x = comparison["mean_temp_C"]
    y = comparison["percentile_days"]
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    plt.plot(x, slope * x + intercept, color= "red", label="Regression line")
    
    textstr = f"r = {r_value:.3f}\np-value = {p_value:.4e}"
    plt.gca().text(
        0.95,
        0.95,
        textstr,
        transform=plt.gca().transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.5)        
    )

    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.xlabel("Annual mean temperature (°C)")
    plt.ylabel("Number of days")
    plt.title(
        f"Annual mean temperature vs. days above {percentile}th percentile"
    )
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "temp_vs_percentile.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

# how heavy rainfall varies by month and season
# mothhly: Scatter

def plot_monthly_temp_vs_rain(comparison):

    plt.figure(figsize=(13, 5))

    plt.scatter(
        comparison["mean_temp_C"],
        comparison["heavy_rain_days"]
    )

    month_mapping = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }

    comparison["month"] = comparison["month"].map(month_mapping)

    for _, row in comparison.iterrows():

        plt.annotate(
            row["month"],
            (
                row["mean_temp_C"],
                row["heavy_rain_days"]
            ),
            xytext=(5, 5),
            textcoords="offset points"
        )

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.xlabel("Monthly mean temperature (°C)")
    plt.ylabel("Number of heavy rainfall days")
    plt.title("Monthly temperature vs. heavy rainfall frequency")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "monthly_temp_vs_rain.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

# seasonal: Scatter

def plot_seasonal_temp_vs_rain(comparison):

    plt.figure(figsize=(13, 4))

    season_mapping = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Autumn"}
    comparison["season"] = comparison["season"].map(season_mapping)

    for season in ["Winter", "Spring", "Summer", "Autumn"]:
        subset = comparison[comparison["season"] == season]
        plt.scatter(
            subset["mean_temp_C"],
            subset["heavy_rain_days"],
            label=season,
            alpha=0.7
        )

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.xlabel("Seasonal mean temperature (°C)")
    plt.ylabel("Number of heavy rainfall days")
    plt.title("Seasonal temperature vs. heavy rainfall frequency")
    plt.legend(title="Seasons")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "seasonal_temp_vs_rain.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

# ================================================================================
# Runoff ?
# ================================================================================

# how rainfall depth and study area influence potential runoff volume

# how different surface assumptions influence the runoff estimate

# how sensitive the results are to the selected assumptions
