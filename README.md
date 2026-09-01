# Long-term changes in daily heavy rainfall and temperature in Bremen

A student project based on a long-term (76 years) geodata from the area of Bremen.
The project shows the relation between climate change, heavy rainfall events and environmental 
engineering. 

============================================================================

## 1. Project summary

The aim of the project is to investigate whether heavy daily rainfall and mean temperature in Bremen 
have changed over time. This investigation could provide evidence for the theoretical links between climate change and the intensification of heavy rain events. 

The project produces:

- A cleaned daily precipitation and temperature dataset of 76 years,
- An analysis of temperature, precipitation & heavy rainfall events and a comparison,
- A visualization of the analysed data,
- A set of figures saved to `reports/figures/`,
- A short results summary printed in the terminal.

============================================================================

## 2. Environmental engineering motivation

Heavy rainfall events are expected to occur with increasing frequency and intensity in the future. These 
events are known for delivering enormous amounts of rain in a very short period of time, which, ideally, 
should seep into the ground. Due to the enormous volumes of water falling in such a short time and the 
increasing amount of impervious surfaces, rainwater often remains on the streets without seeping away. 
The intention is for the rainwater to be collected and drained away through the sewer system. However, 
since sewer systems are often not designed to handle such heavy rainfall events, these enormous volumes 
of water — or at least a portion of them — cannot be drained, which can lead to flooding. The goal of 
this project is therefore to analyze rainfall data from the past 76 years to develop a forecast for the 
future, so that sewer systems can be expanded in a more effective and forward-looking manner.

============================================================================

## 3. Business / company-style problem statement

> **Context.** A small German climate change analytics team wants to assess whether climate change has 
> an effect on heavy rainfall events, their frequency and intensity.
>
> **Question.** Can climate change increase the frequency and intensity of heavy rainfall events?
>
> **Deliverable.** A reproducible Python project that loads 76 years of daily wheater data, analyzes 
> the temperature and precipitation datas, compares them with each other, looks for a statistical 
> correlation between them, and reports the results in a clean way.
============================================================================

## 4. Dataset

The project uses the **E-OBS daily gridded meteorological data for Europe** *Time Series* package, 
release **2020-02-15**. This dataset does not have a downloadable CSV. CSVs are created with the 
notebooks nc_to_csv_precipitation.ipynb and nc_to scv_temperature.ipynb.

- Project page: <https://cds.climate.copernicus.eu/datasets/insitu-gridded-observations-europe?tab=overview>

A smaller cleaned CSV (weather_data.csv) with the needed columns is saved into `data/processed/`.

### 4.1 Selected columns

| Original column              | Renamed to     | Meaning                                      |
|------------------------------|----------------|----------------------------------------------|
| `date`                       | `date`         | Local timestamp at daily resolution          |
| `regional_mean_precip_mm`    | `rain_mm`      | Daily precipitation amount in Bremen, in mm  |
| `regional_mean_temperature_degC`  | `temp_C`  | Daily mean temperature in Bremen, in °C      |

============================================================================

## 5. Project structure
```
vro_project/
│
├── data/
│   ├── raw/                            # large raw files (not committed)
│   └── processed/                      # cleaned & merged dataset
│
├── notebooks/
│   └── nc_to_csv_precipitation.ipynb
│   └── nc_to_csv_temperature.ipynb     # notebooks for converting nc to csv
│
├── reports/
│   └── figures/                        # all generated PNG figures
│
├── src/
│   ├── __init__.py
│   ├── data_preparation.py             # load, clean, time features
│   ├── analysis.py                     # calculations, analysis of the dataset
│   ├── correlation.py                  # correlation between precipitation amount and temperature
│   └── visualization.py                # plotting functions
│
├── .gitignore
├── README.md                           # <-- main documentation
├── requirements.txt
└── main.py                             # main entry point
```
============================================================================

## 6. Setup instructions (Windows, Command Prompt)

Open **Command Prompt** (`cmd.exe`), not PowerShell, and run:

```bat
mkdir vro_project
cd vro_project
code .
python -m venv vro-1
vro-1\Scripts\activate
pip install pandas numpy matplotlib scikit-learn jupyter
pip freeze > requirements.txt
git init
git add .
git commit -m "Initial project structure"
```

Connect the local project to GitHub (replace `USERNAME`):

```bat
git remote add origin https://github.com/amandabueki/vro_project
git branch -M main
git push -u origin main
```

> If you re-open the project later, simply run
> `vro-1\Scripts\activate` from the project folder to re-activate the
> virtual environment.
============================================================================

## 7. How to run the project in VS Code

1. Open the project folder in VS Code (`code .` from Command Prompt).
2. Open a **new terminal** inside VS Code (`Terminal -> New Terminal`). 
   Make sure the terminal type is **Command Prompt**.
3. Activate the virtual environment in that terminal:
   ```bat
   vro-1\Scripts\activate
   ```
4. (Optional) Open `notebooks/nc_to_csv_precipitation.ipynb` & `notebooks/nc_to_csv_temperature.ipynb` 
   and run the cells to verify the environment and the dataset.
5. Run the main script:
   ```bat
   python main.py
   ```
6. Check the generated figures in `reports/figures/` and the cleaned dataset in `data/processed/`.

============================================================================

## 8. Workflow

```
Online NC  ─►  notebooks  ─►  CSV files   ─►  data_preparation  ─►  cleaned dataframe
                                                                           │
                                                                           ▼
                                                                        analysis    ─► calculation of variables for further precesses
                                                                           │
                                                                           ▼
                                                                      correlation    ─► correlation analysis
                                                                           │
                                                                           ▼
                                                                      visualization ─► plotting PNG figures
                                                                           │
                                                                           ▼
                                                                      data/processed/weather_data.csv
```

`main.py` is the orchestrator. It calls the functions from the `src/` package in the order above.

============================================================================


## 9. Results produced by the project

After running `python main.py` you will see:

- A cleaned CSV at data/processed/weather_data.csv,
- A terminal printout with comparison & correlation tables,
- Generated figures from the calculated variables.

============================================================================

## 10. How figures are saved

All figures are produced with matplotlib in the object-oriented style:

```python

output_path = FIGURE_DIR / filename
    plt.tight_layout()
    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )
    ax.plot(...)
   ax.set_xlabel(...)
   ax.set_ylabel(...)
   ax.set_title(...)
    plt.show()
    plt.close()
```

The following figures are saved in `reports/figures/`:

| Filename                          | Content                                                            |
|-----------------------------------|--------------------------------------------------------------------|
| `annual_max_precip.png`           | Maximal rainfall amounts from 1950 to 2025 in Bremen and their distribution relative to the heavy rainfall thresholds                                                   |
| `annual_mean_temp.png`            | Changes in mean temperatures and a trend line from 1950 to 2025 in Bremen                                                                                                   |
| `heavy_rainfall_days.png`         | Number of heavy (≥ 20 mm), intense heavy (≥ 30 mm) and extremely intense heavy rainfall (≥ 40 mm) events in Bremen from 1950 to 2025                                      |
| `monthly_dist.png`                | Monthly distribution of heavy rainfall events from 1950-2025 in Bremen                                                                                                   |
| `monthly_mean_temp.png`           | Monthly mean temperature with measurements from 1950 to 2025 in Bremen                                                                                                   |
| `monthly_temp_vs_rain.png`        | Monthly variarion of heavy rainfall events compared with monthly mean temperature based on measured data from 1950 to 2025 in Bremen                                      |
| `percentile_days.png`             | Annual frequency of days that exceed the 95th or 99th percentile   |
| `seasonal_dist.png`               | Seasonal distribution of heavy rainfall events from 1950-2025 in Bremen                                                                                                   |
| `seasonal_mean_temp.png`          | Seasonal comparison of mean temperatures for the years 1950, 1975, 2000 and 2025 based on measurements in Bremen                                                            |
| `seasonal_temp_vs_rain_20mm.png`  | Seasonal variation of heavy rainfall events with 20 mm/day compared with seasonal mean temperature based on measured data from 1950 to 2025 in Bremen                        |
| `seasonal_temp_vs_rain_30mm.png`  | Seasonal variation of heavy rainfall events with 30 mm/day compared with seasonal mean temperature based on measured data from 1950 to 2025 in Bremen                        |
| `seasonal_temp_vs_rain_40mm.png`  | Seasonal variation of heavy rainfall events with 20 mm/day compared with seasonal mean temperature based on measured data from 1950 to 2025 in Bremen                        |
| `temp_trend`                      | Long term temperature trend from 1950-2025 in Bremen               |
| `temp_vs_95th_percentile.png`     | Annual frequency of extreme precipitation days (above the 95th percentile) compared with annual temperature based on measured data from 1950 to 2025 in Bremen          |
| `temp_vs_99th_percentile.png`     | Annual frequency of extreme precipitation days (above the 95th percentile) compared with annual temperature based on measured data from 1950 to 2025 in Bremen          |
| `temp_vs_heavy_rainfall_20mm.png` | Correlation between mean temperatures and heavy rainfall events with 20 mm/day based on measurements from 1950 to 2025 in Bremen                                         |
| `temp_vs_heavy_rainfall_30mm.png` | Correlation between mean temperatures and heavy rainfall events with 30 mm/day in Bremen from 1950 to 2025                                                               |
| `temp_vs_heavy_rainfall_40mm.png` | Correlation between mean temperatures and heavy rainfall events with 40 mm/day in Bremen from 1950 to 2025                                                               |
| `temp_vs_max_precip.png`          | Correlation between mean temperatures and maximum rainfall totals based on measurements from 1950 to 2025 in Bremen                                                        |

These figures can be inserted directly into the project report.

============================================================================

## 11. References

- Meterological Data. Time series package, version 2020-02-15. https://cds.climate.copernicus.eu/datasets/insitu-gridded-observations-europe?tab=overview
- pandas documentation. https://pandas.pydata.org/docs/
- matplotlib documentation. https://matplotlib.org/stable/