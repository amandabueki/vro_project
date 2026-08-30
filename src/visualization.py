"""
visualization.py

Already calculated values become useful diagrams for the report.
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from scipy import stats
from pathlib import Path

# path for saving graphs

FIGURE_DIR = Path("reports/figures")
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# ================================================================================
# Helper functions
# ================================================================================

def save_and_close(filename):

    output_path = FIGURE_DIR / filename
    plt.tight_layout()
    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()
    plt.close()

def valid_xy(data, x_column, y_column):

    required_columns = [x_column, y_column]
    missing = [
        column for column in required_columns
        if column not in data.columns
    ]
    if missing:
        raise KeyError(
            f"Missing required column(s): {missing}"
        )

    return data[required_columns].dropna()

def season_labels():

    return {
        1: "Winter",
        2: "Spring",
        3: "Summer",
        4: "Autumn"
    }

def month_labels():

    return {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    }

# ================================================================================
# Temperature
# ================================================================================

# anual mean temperature

def plot_annual_mean_temp(annual_temp):

    data = annual_temp[
        ["year", "mean_temp_C"]
    ].dropna()

    plt.figure(figsize=(10, 5))

    plt.plot(
        data["year"],
        data["mean_temp_C"],
        marker="o",
        markersize=3,
        linewidth=1,
        label="Annual mean temperature"
    )

    m, b = np.polyfit(data["year"], data["mean_temp_C"], 1)

    plt.plot(
        data["year"],
        m * data["year"] + b,
        color="red",
        linestyle="-",
        linewidth=2,
        label="Linear trend"
    )

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.xlabel("Year")
    plt.ylabel("Mean temperature (°C)")
    # plt.title("Annual mean temperature")
    plt.grid(True, alpha=0.3)
    plt.legend()
    save_and_close("annual_mean_temp.png")

# seasonal mean temperature

def plot_seasonal_mean_temp(seasonal_temp):

    required_columns = [
        "year",
        "season",
        "mean_temp_C"
    ]

    missing = [
        column 
        for column in required_columns
        if column not in seasonal_temp.columns
    ]

    if missing:
        raise KeyError(
            f"Missing required column(s): {missing}"
        )

    selected_years = [1950, 1975, 2000, 2025]

    plt.figure(figsize=(9, 6))

    for year in selected_years:

        year_data = seasonal_temp[
            seasonal_temp["year"] == year
        ].sort_values("season")

        if year_data.empty:
            continue

        plt.plot(
            year_data["season"],
            year_data["mean_temp_C"],
            label=str(year),
            marker='o',
            markersize=6
        )

    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.xticks(ticks=[1, 2, 3, 4], labels=["Winter", "Spring", "Summer", "Autumn"])
    plt.xlabel("Season")
    plt.ylabel("Mean temperature (°C)")
    # plt.title("Seasonal mean temperature (°C) in selected years")
    plt.legend(title="Year")
    plt.grid(True, alpha=0.3)
    save_and_close("seasonal_mean_temp.png")

# temperature trend

def plot_temp_trend(annual_temp, trend):

    data = annual_temp[
        ["year", "mean_temp_C"]
    ].dropna()

    if data.empty:
        return

    slope = trend.get(
        "slope_C_per_year",
        np.nan
    )

    intercept = trend.get(
        "intercept",
        np.nan
    )

    plt.figure(figsize=(10, 5))

    plt.scatter(
        data["year"],
        data["mean_temp_C"],
        s=20,
        label="Annual mean temperature"
    )

    if not np.isnan(slope) and not np.isnan(intercept):

        trend_values = (
            slope * data["year"]
            + intercept
        )

    plt.plot(
        data["year"],
        trend_values,
        color="red",
        linestyle="-",
        linewidth=2,
        label="Linear trend"
    )

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.xlabel("Year")
    plt.ylabel("Mean temperature (°C)")
    # plt.title("Annual temperature trend")
    plt.legend()
    plt.grid(True, alpha=0.3)
    save_and_close("temp_trend.png")

# ================================================================================
# Precipitation
# ================================================================================

# whether heavy rainfall indicators changed
# maximum daily precipitation

def plot_annual_max_precip(max_precip):

    data = max_precip[
        ["year", "max_precip_mm"]
    ].dropna()

    plt.figure(figsize=(10, 5))

    plt.plot(
        data["year"],
        data["max_precip_mm"],
        marker="o",
        markersize=3,
        linewidth=1,
        label="Maximum daily precipitation"
    )

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.xlabel("Year")
    plt.ylabel("Maximum daily precipitation (mm)")
    plt.axhline(y=20, color="yellow", linestyle='--', linewidth=1, label='Heavy rainfall (20mm/day)')
    plt.axhline(y=30, color="orange", linestyle='--', linewidth=1, label='Intense heavy rainfall (30mm/day)')
    plt.axhline(y=40, color="red", linestyle='--', linewidth=1, label='Extreme intense heavy rainfall (40mm/day)')
    plt.legend()
    # plt.title("Annual maximum daily precipitation")
    plt.grid(True, alpha=0.3)
    save_and_close("annual_max_precip.png")

# heavy rainfall days with 20, 30 and 40 mm

def plot_heavy_rainfall_days(days20, days30, days40):

    data20 = days20[
        ["year", "heavy_rain_days_20"]
    ].dropna()

    data30 = days30[
        ["year", "heavy_rain_days_30"]
    ].dropna()

    data40 = days40[
        ["year", "heavy_rain_days_40"]
    ].dropna()

    plt.figure(figsize=(10, 5))

    plt.plot(
        data20["year"],
        data20["heavy_rain_days_20"],
        label="≥ 20 mm/day",
        color="yellow"
    )

    plt.plot(
        data30["year"],
        data30["heavy_rain_days_30"],
        label="≥ 30 mm/day",
        color="orange"
    )

    plt.plot(
        data40["year"],
        data40["heavy_rain_days_40"],
        label="≥ 40 mm/day",
        color="red"
    )

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.xlabel("Year")
    plt.ylabel("Number of days")
    # plt.title("Annual frequency of heavy rainfall days")
    plt.legend()
    plt.grid(True, alpha=0.3)
    save_and_close("heavy_rainfall_days.png")

# percentile days with precipitation over the 95th and 99th percentile

def plot_percentile_days(days95, days99):

    column95 = "days_above_95th_percentile"
    column99 = "days_above_99th_percentile"

    if column95 not in days95.columns:
        raise KeyError(
            f"Missing required column in days95: {column95}. "
            f"Available columns: {list(days95.columns)}"
        )
    if column99 not in days99.columns:
        raise KeyError(
            f"Missing required column in days99: {column99}. "
            f"Available columns: {list(days99.columns)}"
        )

    data95 = days95[
        ["year", column95]
    ].dropna()

    data99 = days99[
        ["year", column99]
    ].dropna()

    data95 = data95.sort_values("year")
    data99 = data99.sort_values("year")

    plt.figure(figsize=(10, 5))

    plt.plot(
        data95["year"],
        data95[column95],
        label="95th percentile",
        linewidth=1.5
    )

    plt.plot(
        data99["year"],
        data99[column99],
        label="99th percentile",
        linewidth=1.5
    )

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.xlabel("Year")
    plt.ylabel("Number of days")
    # plt.title("Annual frequency of extreme precipitation days")
    plt.legend()
    plt.grid(True,alpha=0.3)
    save_and_close("percentile_days.png")

# monthly distribution of heavy rainfall events

def plot_monthly_dist(monthly_dist):

    data = monthly_dist[
        ["month",
         "heavy_rain_days_20",
         "heavy_rain_days_30",
         "heavy_rain_days_40"]
    ].dropna()

    data = data.sort_values("month")

    x = np.arange(len(data))
    width = 0.22

    plt.figure(figsize=(10, 5))


    plt.bar(
        x - width,
        data["heavy_rain_days_20"],
        width,
        label="≥ 20 mm/day",
        color="yellow"
    )

    plt.bar(
        x,
        data["heavy_rain_days_30"],
        width,
        label="≥ 30 mm/day",
        color="orange"
    )

    plt.bar(
        x + width,
        data["heavy_rain_days_40"],
        width,
        label="≥ 40 mm/day",
        color="red"
    )

    month_mapping = month_labels()

    labels = [
        month_mapping.get(
            int(month),
            str(month)
        )
        for month in data["month"]
    ]

    plt.xticks(x, labels)
    plt.xlabel("Month")
    plt.ylabel("Number of heavy rainfall days")
    plt.legend()
    # plt.title("Monthly distribution of heavy rainfall")
    plt.grid(True, axis='y', alpha=0.3)
    save_and_close("monthly_dist.png")

# seasonal distribution of heavy rainfall events

def plot_seasonal_dist(seasonal_dist):

    required_columns = [
        "season",
        "heavy_rain_days_20",
        "heavy_rain_days_30",
        "heavy_rain_days_40"
    ]

    missing = [
        column 
        for column in required_columns
        if column not in seasonal_dist.columns
    ]

    if missing:
        raise KeyError(
            f"Missing required column(s): {missing}"
        )

    data = seasonal_dist.copy()

    if "year" in data.columns:

        data = (
            data.groupby("season", as_index=False)[
                ["heavy_rain_days_20",
                 "heavy_rain_days_30",
                 "heavy_rain_days_40"]
            ]
            .sum()
        )

    data = data.sort_values("season")

    x = np.arange(len(data))
    width = 0.25

    plt.figure(figsize=(10, 5))

    plt.bar(
        x - width,
        data["heavy_rain_days_20"],
        width,
        label="≥ 20 mm/day",
        color="yellow"
    )

    plt.bar(
        x,
        data["heavy_rain_days_30"],
        width,
        label="≥ 30 mm/day",
        color="orange"
    )

    plt.bar(
        x + width,
        data["heavy_rain_days_40"],
        width,
        label="≥ 40 mm/day",
        color="red"
    )

    season_mapping = season_labels()

    labels = [
        season_mapping.get(
            int(season),
            str(season)
        )
        for season in data["season"]
    ]
    plt.xticks(x, labels)

    plt.xlabel("Season")
    plt.ylabel("Mean number of heavy rainfall days")
    plt.legend()
    # plt.title("Seasonal distribution of heavy rainfall")
    plt.grid(True, axis='y', alpha=0.3)
    save_and_close("seasonal_dist.png")

# maximum consecutive precipitation over 3 or 5 days

def plot_max_consecutive_precip(max3, max5):

    data3 = max3[
        ["year", "max_3_day_precip_mm"]
    ].dropna()

    data5 = max5[
        ["year", "max_5_day_precip_mm"]
    ].dropna()

    plt.figure(figsize=(10, 5))

    plt.plot(
        data3["year"],
        data3["max_3_day_precip_mm"],
        label="Maximum 3-day precipitation"
    )

    plt.plot(
        data5["year"],
        data5["max_5_day_precip_mm"],
        label="Maximum 5-day precipitation"
    )

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.xlabel("Year")
    plt.ylabel("Precipitation (mm)")
    # plt.title("Maximum precipitation over consecutive days")
    plt.legend()
    plt.grid(True, alpha=0.3)
    save_and_close("max_consecutive_precip.png")

# ================================================================================
# Relationsships
# ================================================================================

# whether temperature and rainfall indicators are statistically associated
# temperature vs. maximum rainfall

def plot_temp_vs_max_precip(comparison):

    data = valid_xy(
        comparison,
        "mean_temp_C",
        "max_precip_mm"
    )

    plt.figure(figsize=(10, 5))

    x = data["mean_temp_C"]
    y = data["max_precip_mm"]

    plt.scatter(
        x,
        y,
        label="Maximal precipitation amount (mm)"
    )

    if len(data) >= 2 and x.nunique() > 1:
        regression = stats.linregress(
            x,
            y
        )

        x_line = np.linspace(
            x.min(),
            x.max(),
            100
        )

        y_line = (
            regression.slope * x_line + regression.intercept
        )

        plt.plot(
            x_line,
            y_line,
            color="red",
            label="Regression line"
        )

        textstr = (
            f"r = {regression.rvalue:.3f}\n"
            f"p-value = {regression.pvalue:.4e}"
        )

        plt.gca().text(
            0.95,
            0.95,
            textstr,
            transform=plt.gca().transAxes,
            verticalalignment="top",
            horizontalalignment="right",
            bbox=dict(
                boxstyle="round, pad=0.5",
                facecolor="white",
                alpha=0.5
            )
        )

        plt.legend(loc="upper left")
    
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.xlabel("Annual mean temperature (°C)")
    plt.ylabel("Annual maximum precipitation (mm)")
    # plt.title("Annual mean temperature vs. annual maximum precipitation")
    plt.grid(True, alpha=0.3)
    save_and_close("temp_vs_max_precip.png")

# temperature vs. heavy rainfall days

def plot_temp_vs_heavy_rainfall(comparison, threshold=30):

    column = (f"heavy_rain_days_{threshold}")

    data = valid_xy(
        comparison,
        "mean_temp_C",
        column
    )

    plt.figure(figsize=(10, 5))

    x = data["mean_temp_C"]
    y = data[column]

    plt.scatter(
        x, 
        y,
        label=f"Heavy rainfall days ≥ {threshold} mm"
    )

    if len(data) >= 2 and x.nunique() > 1:
        regression = stats.linregress(
            x,
            y
        )

        x_line = np.linspace(
            x.min(),
            x.max(),
            100
        )

        y_line = (
            regression.slope * x_line + regression.intercept
        )

        plt.plot(
            x_line,
            y_line,
            color="red",
            label="Regression line"
        )

        textstr = (
            f"r = {regression.rvalue:.3f}\n"
            f"p-value = {regression.pvalue:.4e}"
        )

        plt.gca().text(
            0.95,
            0.95,
            textstr,
            transform=plt.gca().transAxes,
            verticalalignment="top",
            horizontalalignment="right",
            bbox=dict(
                boxstyle="round, pad=0.5",
                facecolor="white",
                alpha=0.5
            )
        )

        plt.legend()

    plt.xlabel("Annual mean temperature (°C)")
    plt.ylabel("Number of heavy rainfall days")
    # plt.title(f"Annual mean temperature vs. days ≥ {threshold} mm/day")
    plt.grid(True, alpha=0.3)
    save_and_close(f"temp_vs_heavy_rainfall_{threshold}mm.png")

# temperature vs. 95 percentile days

def plot_temp_vs_percentile(comparison, percentile=95):

    column = (f"days_above_{percentile}th_percentile")

    data = valid_xy(
        comparison,
        "mean_temp_C",
        column
    )

    plt.figure(figsize=(10, 5))

    x = data["mean_temp_C"]
    y = data[column]

    plt.scatter(
        x,
        y,
        label=f"Days above the {percentile}th percentile"
    )

    if len(data) >= 2 and x.nunique() > 1:

        regression = stats.linregress(
            x,
            y
        )

        x_line = np.linspace(
            x.min(),
            x.max(),
            100
        )

        y_line = (
            regression.slope * x_line + regression.intercept
        )

        plt.plot(
            x_line,
            y_line,
            color="red",
            label="Regression line"
        )

        textstr = (
            f"r = {regression.rvalue:.3f}\n"
            f"p-value = {regression.pvalue:.4e}"
        )

        plt.gca().text(
            0.95,
            0.95,
            textstr,
            transform=plt.gca().transAxes,
            verticalalignment="top",
            horizontalalignment="right",
            bbox=dict(
                boxstyle="round, pad=0.5",
                facecolor="white",
                alpha=0.5
            )
        )

        plt.legend()

    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.xlabel("Annual mean temperature (°C)")
    plt.ylabel("Number of days")
    # plt.title(f"Annual mean temperature vs. days above {percentile}th percentile")
    plt.grid(True, alpha=0.3)
    save_and_close(f"temp_vs_{percentile}th_percentile.png")

# how heavy rainfall varies by month and season
# mothhly

def plot_monthly_temp_vs_rain(comparison):

    required_columns = [
        "month",
        "mean_temp_C",
        "heavy_rain_days_20",
        "heavy_rain_days_30",
        "heavy_rain_days_40"
    ]

    missing = [
        c
        for c in required_columns
        if c not in comparison.columns
    ]

    if missing:
        raise KeyError(
            f"Missing required column(s): {missing}. "
            f"Available columns: {list(comparison.columns)}"
        )

    data = comparison[
        required_columns
    ].dropna().copy()

    data = data.sort_values("month")

    if data.empty:
        print(
            "No valid data available for "
            "monthly temperature vs. rainfall plot."
        )
        return

    plt.figure(figsize=(13, 6))

    x = data["mean_temp_C"]

    plt.scatter(
        x,
        data["heavy_rain_days_20"],
        color="yellow",
        label="≥ 20 mm/day"
    )

    plt.scatter(
        x,
        data["heavy_rain_days_30"],
        color="orange",
        label="≥ 30 mm/day"
    )

    plt.scatter(
        x,
        data["heavy_rain_days_40"],
        color="red",
        label="≥ 40 mm/day"
    )

    rainfall_columns = {
        "heavy_rain_days_20": ("≥ 20 mm/day", "yellow"),
        "heavy_rain_days_30": ("≥ 30 mm/day", "orange"),
        "heavy_rain_days_40": ("≥ 40 mm/day", "red")
    }

    for column, (label, color) in rainfall_columns.items():

        y = data[column]

        if len(data) >= 2 and x.nunique() > 1:

            regression = stats.linregress(x, y)

            x_line = np.linspace(
                x.min(),
                x.max(),
                100
            )

            y_line = (
                regression.slope * x_line
                + regression.intercept
            )

            plt.plot(
                x_line,
                y_line,
                color=color,
                linestyle="--",
                label=f"Trend {label}"
            )

    month_mapping = month_labels()

    for _, row in data.iterrows():

        month_number = int(row["month"])

        month_label = month_mapping.get(
            month_number,
            str(month_number)
        )

        plt.annotate(
            month_label,
            (
                row["mean_temp_C"],
                row["heavy_rain_days_20"]
            ),
            xytext=(5, 5),
            textcoords="offset points"
        )

        plt.annotate(
            month_label,
            (
                row["mean_temp_C"],
                row["heavy_rain_days_30"]
            ),
            xytext=(5, 5),
            textcoords="offset points"
        )

        plt.annotate(
            month_label,
            (
                row["mean_temp_C"],
                row["heavy_rain_days_40"]
            ),
            xytext=(5, 5),
            textcoords="offset points"
        )    

    plt.xlabel("Monthly mean temperature (°C)")
    plt.ylabel("Number of heavy rainfall days")
    # plt.title("Monthly mean temperature vs. heavy rainfall frequency")
    plt.legend(loc="upper left")
    plt.grid(True, alpha=0.3)
    save_and_close("monthly_temp_vs_rain.png")

# seasonal

def plot_seasonal_temp_vs_rain(comparison, threshold=30):

    column = (
        f"heavy_rain_days_{threshold}"
    )

    required_columns = [
        "season",
        "mean_temp_C",
        column
    ]

    missing = [
        c
        for c in required_columns
        if c not in comparison.columns
    ]

    if missing:
        raise KeyError(
            f"Missing required column(s): {missing}"
        )

    data = comparison[
        required_columns
    ].dropna().copy()

    season_mapping = season_labels()

    plt.figure(figsize=(13, 5))

    for season_number in [1, 2, 3, 4]:

        subset = data[
            data["season"] == season_number
        ]

        if subset.empty:
            continue

        season_label = season_mapping.get(
            season_number,
            str(season_number)
        )

        plt.scatter(
            subset["mean_temp_C"],
            subset[column],
            label=season_label,
            alpha=0.7
        )

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.xlabel("Seasonal mean temperature (°C)")
    plt.ylabel(f"Number of heavy rainfall days with ≥ {threshold} mm")
    # plt.title(f"Seasonal temperature vs. heavy rainfall frequency ≥ {threshold} mm/day")
    plt.legend(title="Seasons")
    plt.grid(True, alpha=0.3)
    save_and_close(f"seasonal_temp_vs_rain_{threshold}mm.png")