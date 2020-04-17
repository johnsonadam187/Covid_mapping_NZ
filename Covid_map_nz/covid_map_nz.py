from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)



def plot_growth_rate(filepath, rolling_number):
    """takes in filepath to excel files, and a number for rolling average days, cleans data and plots"""

    df_confirmed = pd.read_excel(
        filepath,
        sheet_name="Confirmed", header=3)
    df_probable = pd.read_excel(
        filepath,
        sheet_name="Probable", header=3)
    df_combined = pd.concat([df_confirmed, df_probable], sort=True)
    df_combined.reset_index(drop=True, inplace=True)
    df_combined['Overseas travel'].replace([np.NaN, 'No', "Unknown"], 'Community', inplace=True)
    no_intl_travel = len(df_combined[df_combined['Overseas travel'] == 'Community'])
    percent_community_transmission = no_intl_travel / len(df_combined) * 100
    df_combined["Last country before return"].replace(np.NaN, "Community", inplace=True)
    df_intl_source = df_combined["Last country before return"].value_counts()
    non_community_cases = df_intl_source.sum() - df_intl_source['Community']
    potential_infectivity = df_intl_source['Community'] / non_community_cases
    df_dates = df_combined["Date of report"].copy()
    df_dates = pd.to_datetime(df_dates, format='%d/%m/%Y')
    new_cases = np.ones(len(df_dates), dtype=int)
    series_new_cases = pd.Series(new_cases, name="New Cases")
    df_date_sort = pd.concat([df_dates, series_new_cases], axis=1)
    df_date_sort.sort_values(by="Date of report", ascending=True, inplace=True)
    df_date_sort = df_date_sort.groupby("Date of report")
    new_cases_per_date = df_date_sort.sum()
    index_number = len(new_cases_per_date) - rolling_number
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=(8, 10))
    new_cases_per_date.plot(style="--", ax=ax1, rot=90)
    ax1.set_title("New cases")
    rolling = new_cases_per_date.rolling(rolling_number).mean()
    rolling.plot(style='k-', ax=ax2, rot=90)
    ax2.set_title(f"Rolling average ({rolling_number} days)")
    rolling_new = np.array(rolling).reshape(-1)
    derivative = np.diff(rolling_new)
    ax3.plot(derivative)
    ax3.set_title("Slope of growth rate")
    ax3.set_xticks(range(len(new_cases_per_date[1:])))
    xlabels = [str(item).replace('T00:00:00.000000000', '') for item in np.array(new_cases_per_date.index[1:])]
    ax3.set_xticklabels(xlabels, rotation=75)
    plt.tight_layout()
    plt.show()

for num in range(1,8):
    plot_growth_rate('https://www.health.govt.nz/system/files/documents/pages/covid-19-case-list-17-april-2020.xlsx', num)




