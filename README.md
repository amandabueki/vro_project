# Analysis of changes in heavy rainfall, regional temperature, and potential 
# runoff volumes in Bremen

A student project based on a long-term (75 years) geodata from the area of 
Bremen. The project shows the relation between climate change, heavy rainfall 
events and environmental enginerring. 

============================================================================


## 1. Project summary

The aim of the project is to investigate whether heavy daily rainfall and mean 
temperature in Bremen have changed over time. Selected temperature and 
precipitation data are used to carry out a simplified assessment of heavy 
rainfall events (& potential runoff volumes under different hypothetical surface 
conditions.) # <= es steht zwar in Abbys Mail, ist aber nur schwierig zu 
untersuchen, denn wir wissen nicht, wie viel Wasser versickert und oder wie viel 
abgeleitet wird #

The project produces:

- A cleaned daily precipitation and temperature dataset of 75 years.
- An analysis of temperature, precipitation & heavy rainfall events and a 
   comparison.
- A visualization of the analysed data.
- A set of figures saved to `reports/figures/`.
- A short results summary printed in the terminal.

============================================================================

## 2. Environmental engineering motivation

Heavy rainfall events are expected to occur with increasing frequency and 
intensity in the future. These events are known for delivering enormous 
amounts of rain in a very short period of time, which, ideally, should seep 
into the ground. Due to the enormous volumes of water falling in such a short 
time and the increasing amount of impervious surfaces, rainwater often 
remains on the streets without seeping away. The intention is for the 
rainwater to be collected and drained away through the sewer system. However, 
since sewer systems are often not designed to handle such heavy rainfall 
events, these enormous volumes of water — or at least a portion of them — 
cannot be drained, which can lead to flooding. The goal of this project is 
therefore to analyze rainfall data from the past 75 years to develop a 
forecast for the future, so that sewer systems can be expanded in a more 
effective and forward-looking manner.

============================================================================


## 3. Business / company-style problem statement

> **Context.** A small German climate change analytics team wants to assess 
> whether climate change has an effect on heavy rainfall events, their 
> frequency and intensity. 
>
> **Question.** Can climate change increase the frequency and intensity 
> of heavy rainfall events?
>
> **Deliverable.** A reproducible Python project that loads 75 years of 
> daily wheater data, analyzes the temperature and precipitation datas, 
> compares them with each other, looks for a statistical correlation between 
> them, and reports the results in a clean way.

============================================================================

## 4. Dataset

The project uses the **E-OBS daily gridded meteorological data for Europe** 
*Time Series* package, release **2020-02-15**. This dataset does not have a 
downloadable CSV. CSVs are created with the notebooks 
`nc_to_csv_precipitation.ipynb` (`bremen_daily_mean_temperature.csv`) and 
`nc_to scv_temperature.ipynb` (`bremen_daily_precipitation.csv`), they were 
merged (`merged_data.csv`) and saved into `data/processed`.

- Project page: <https://cds.climate.copernicus.eu/datasets/insitu-gridded-observations-europe?tab=overview>

A smaller cleaned CSV (`weather_data.csv`) with the needed columns is saved 
into `data/processed/`.

### 4.1 Selected columns

Selected columns from the original files:

| Original column              | Renamed to  | Meaning                                      |
|------------------------------|-------------|----------------------------------------------|
| `date`                       | `date`      | Local timestamp at daily resolution          |
| `selected_precip_mm`         | `rain_mm`   | Daily precipitation amount in Bremen, in mm  |
| `selected_temperature_degC`  | `temp_C`    | Daily mean temperature in Bremen, in °C      |

Since thresholds for heavy rainfall events are defined based on amounts 
within 1 and 6 hours, and the dataset only contains daily values, the 
average precipitation amounts within one and six hours were calculated for 
each days using the original column and added to the new CSV.

| Created column  | Created through  | Meaning                                     |
|-----------------|------------------|---------------------------------------------|
| `rain_6_mm`     | `rain_mm` / 4    | Calculated precipitation amount in 6 hours  |
| `rain_1_mm`     | `rain_mm` / 24   | Calculated precipitation amount in 1 hour   |

### 4.2 Citation

?

(> Open Power System Data. 2020. Data Package Time series.)
(> Version 2020-10-06. <https://data.open-power-system-data.org/time_series/2020-10-06/>. )
(> (Primary data from various sources, see project page.) )

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
│   ├── figures/                        # all generated PNG figures
│   └── report_outline.md               # writing guide for the ~20-page report
│
├── src/
│   ├── __init__.py
│   ├── data_preparation.py             # load, clean, time features
│   ├── analysis.py                     # calculations, analysis of the dataset
│   ├── evaluation.py                   # correlation between precipitation amount and temperature
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
git remote add origin https://github.com/USERNAME/vro_project.git
git branch -M main
git push -u origin main
```

> If you re-open the project later, simply run `vro-1\Scripts\activate` from 
> the project folder to re-activate the virtual environment.

============================================================================

## 7. How to run the project in VS Code

1. Open the project folder in VS Code (`code .` from Command Prompt).
2. Open a **new terminal** inside VS Code (`Terminal -> New Terminal`). 
   Make sure the terminal type is **Command Prompt**.
3. Activate the virtual environment in that terminal:
   ```bat
   vro-1\Scripts\activate
   ```
4. (Optional) Open `notebooks/nc_to_csv_precipitation.ipynb` & 
   `notebooks/nc_to_csv_temperature.ipynb` and run the cells to verify the 
   environment and the dataset.
5. Run the main script:
   ```bat
   python main.py
   ```
6. Check the generated figures in `reports/figures/` and the cleaned dataset 
in `data/processed/`.

============================================================================

## 8. Workflow

```
Online NC  ─►  notebooks  ─►  CSV files   ─►  data_preparation  ─►  cleaned dataframe
                                                                           │
                                                                           ▼
                                                                        analysis    ─► 
                                                                           │
                                                                           ▼
                                                                      evaluation    ─► 
                                                                           │
                                                                           ▼
                                                                      visualization ─► plotting PNG figures
                                                                           │
                                                                           ▼
                                                                      data/processed/weather_data.csv
```

`main.py` is the orchestrator. It calls the functions from the `src/` 
package in the order above.

============================================================================

## 9. Baseline forecasting methods

?

This project uses **only simple, transparent baselines** – no machine
learning. The methods are:

1. **Yesterday-same-hour.**
   The forecast for hour *t* equals the actual load at hour *t − 24h*.
   *Idea:* electricity demand has a strong daily pattern.

2. **Last-week-same-hour.**
   The forecast for hour *t* equals the actual load at hour *t − 168h*
   (7 days). *Idea:* demand also has a weekly pattern (workdays
   vs. weekends).

3. **Rolling 24-hour average.**
   The forecast for hour *t* equals the average of the previous 24
   actual values. *Idea:* a smoothed recent level.

All three are compared against the **official day-ahead forecast**
already provided in the dataset.

============================================================================

## 10. Results produced by the project

After running `python main.py` you will see:

- A terminal printout with the comparison table:
- A short summary highlighting the best baseline method.
- A cleaned CSV at `data/processed/weather_data.csv`.

============================================================================

## 11. How figures are saved

All figures are produced with matplotlib in the object-oriented style:

```python
fig, ax = plt.subplots()
ax.plot(...)
ax.set_xlabel(...)
ax.set_ylabel(...)
ax.set_title(...)
fig.savefig("reports/figures/<name>.png", dpi=300)
```

The following figures are saved in `reports/figures/`:

| Filename                      | Content                                                                   |
|-------------------------------|---------------------------------------------------------------------------|
| `annual_max_precip.png`       | Maximal precipitation amount (mm) of each year                            |
| `annual_mean_temp.png`        | Mean temperature (°C) of each year                                        |
| `heavy_rainfall_days.png`     | Annual frequency of heavy rainfall days                                   |
| `max_consecutive_precip.png`  | Maximum consecutive precipitation over three or five days                 |
| `monthly_dist.png`            | Monthly distribution of heavy rainfall events                             |
| `monthly_temp_vs_rain.png`    | Monthly variation of heavy rainfall events compared with temperature      |
| `percentile_days.png`         | Annual frequency of extreme precipitation days                            |
| `seasonal_dist.png`           | Seasonal distribution of heavy rainfall events                            |
| `seasonal_mean_temp.png`      | Seasonal mean temperature (°C)                                            |
| `seasonal_temp_vs_rain.png`   | Seasonal variation of heavy rainfall events compared with temperature     |
| `temp_trend.png`              | Trend of temperature change                                               |
| `temp_vs_heavy_rainfall.png`  | Annual mean temperature compared with heavy rainfall days                 |
| `temp_vs_max_precip.png`      | Annual maximum precipitation compared with mean temperature               |
| `temp_vs_percentile.png`      | Annual frequency of extreme precipitation days compared with temperature  |

These figures can be inserted directly into the project report.

Ich würde das hier löschen, weil wir keine machine-learning machen wollen(?)
(## 12. Future machine-learning extension

The project is intentionally simple, but it is structured so that an
ML extension can be added later without rewriting everything:

- `src/data_preparation.py` already produces useful features
  (`hour`, `day_of_week`, `month`, …).
- `src/forecasting.py` could be extended with, for example:
  - Linear regression on the time features.
  - A regression tree or random forest.
  - A gradient boosting model.
  - A small recurrent neural network.
- `src/evaluation.py` and the comparison table can stay the same –
  any new model is just one more row in the table.

This makes the project a natural starting point for a follow-up
course on data-driven energy analytics.)

## 12. Future plans with the project

- Some graphs could not be plotted because of the small values of the 
   created columns `rain_6_mm/h` and `rain_1_mm/h`. We will work on a 
   solution for being able to plot those graphs as well and still be 
   precise. 
- Furthermore, we are still working on the report, therefore it is not 
   clear yet, which graphs, comparisons & correlations we will need 
   for our final project. That means, that some analysis will be changed 
   or completely replaced, however, the structure of the project remains.

============================================================================

## 13. References

- Meterological Data. *Time series* package, version 2020-02-15.
  <https://cds.climate.copernicus.eu/datasets/insitu-gridded-observations-europe?tab=overview>
- pandas documentation. <https://pandas.pydata.org/docs/>
- matplotlib documentation. <https://matplotlib.org/stable/>

