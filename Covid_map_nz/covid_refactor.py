from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def create_df(filepath):
    df_confirmed = pd.read_excel(
        filepath,
        sheet_name="Confirmed", header=3)
    df_probable = pd.read_excel(
        filepath,
        sheet_name="Probable", header=3)
    return df_confirmed, df_probable

def clean_df(dataframe1, dataframe2):
    df3 = pd.concat([dataframe1, dataframe2], sort=True)
    df3.reset_index(drop=True, inplace=True)
    df3['Overseas travel'].replace([np.NaN, 'No', "Unknown", " "], 'Community', inplace=True)
    df3["Last country before return"].replace(np.NaN, "Community", inplace=True)
    return df3

def reformat_df(dataframe):
    df_dates = dataframe["Date of report"].copy()
    df_dates = pd.to_datetime(df_dates, format='%d/%m/%Y')
    new_cases = np.ones(len(df_dates), dtype=int)
    series_new_cases = pd.Series(new_cases, name="New Cases")
    df_date_sort = pd.concat([df_dates, series_new_cases], axis=1)
    df_date_sort.sort_values(by="Date of report", ascending=True, inplace=True)
    new_cases_per_date = df_date_sort.groupby("Date of report").sum()
    return new_cases_per_date

def plot_growth_and_rate(dataframe, rolling_number):
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=(8, 10))
    dataframe.plot(style="--", ax=ax1, rot=90)
    ax1.set_title("New cases")
    rolling = dataframe.rolling(rolling_number).mean()
    rolling.plot(style='k-', ax=ax2, rot=90)
    ax2.set_title(f"Rolling average ({rolling_number} days)")
    rolling_new = np.array(rolling).reshape(-1)
    derivative = np.diff(rolling_new)
    ax3.plot(derivative)
    ax3.set_title("Slope of growth rate")
    ax3.set_xticks(range(len(dataframe[1:])))
    xlabels = [str(item).replace('T00:00:00.000000000', '') for item in np.array(dataframe.index[1:])]
    ax3.set_xticklabels(xlabels, rotation=75)
    plt.tight_layout()
    plt.show()

def clean_recoveries_data(filepath2, dataframe):
    """ Plots cumulative cases, recovered, and active cases over time, requires manual entry of new recoveries as not
             listen in MOH page"""

    recover = pd.read_csv(filepath2, index_col=0)
    cumulative_new_cases = dataframe.cumsum()
    recoveries = recover.iloc[1, :].copy()
    recoveries['10/04/2020'] = 373
    recoveries['11/04/2020'] = 422
    recoveries['12/04/2020'] = 471
    recoveries['13/04/2020'] = 546
    recoveries['14/04/2020'] = 628
    recoveries['15/04/2020'] = 728
    recoveries['16/04/2020'] = 770
    recoveries['17/04/2020'] = 816
    recoveries['18/04/2020'] = 912
    recoveries['19/04/2020'] = 974
    # TODO sort out deaths and add to the plotting



if __name__ == "__main__":
    df_obj1, df_obj2 = create_df('https://www.health.govt.nz/system/files/documents/pages/covid-caselist-20april.xlsx')
    df_clean = clean_df(df_obj1, df_obj2)
    cases_per_date_df = reformat_df(df_clean)
    plot_growth_and_rate(cases_per_date_df, 7)