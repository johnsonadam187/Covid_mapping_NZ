from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def covid_plotting():


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
        print(f"No sign of international travel: {no_intl_travel}")
        print(f'Community transmission as percentage of all cases: {percent_community_transmission:.2f} %')
        print(f'Potential infectivity: {potential_infectivity}')
        print(f'International travel Cases: {non_community_cases}')
        print(df_intl_source.to_string())
        return new_cases_per_date
    new_cases_per_date = plot_growth_rate('https://www.health.govt.nz/system/files/documents/pages/covid-19-case-list-17-april-2020.xlsx', 7)

    def plot_active_cases(filepath, dataframe):
        """ Plots cumulative cases, recovered, and active cases over time, requires manual entry of new recoveries as not
         listen in MOH page"""

        recover = pd.read_csv(filepath, index_col=0)
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

        new_index = [item.strftime("%d/%m/%Y") for item in
                     cumulative_new_cases.index]  # reformat dates into correct format from Cumulative
        new_index = pd.Series(new_index, name="Date")  # create a Series for the DataFrame
        cumulative_new_cases.reset_index(drop=True, inplace=True)  # delete the index for concatenation
        new_cases = pd.concat([new_index, cumulative_new_cases],
                              axis=1)  # create a new dataframe with the dates as a column
        recov = recoveries[
            recoveries.index.isin(new_cases["Date"])]  # filter recoveries by dates available in cumulative_new_cases
        recov.fillna(value=0, inplace=True)  # fill NaN values with a 0 for later calculations
        new_cases = new_cases[new_cases['Date'].isin(recov.index)]  # filter new_cases by dates in recoveries
        new_cases.reset_index(drop=True, inplace=True)
        recov.reset_index(drop=True, inplace=True)
        new_cases['Recoveries'] = recov
        new_cases["Active Cases"] = new_cases["New Cases"] - new_cases["Recoveries"]
        new_cases.set_index("Date", inplace=True)
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True, figsize=(8, 10))
        ax1.plot(new_cases["New Cases"], 'b--')
        ax1.set_title("New Cases")
        ax2.plot(new_cases["Recoveries"], 'r--')
        ax2.set_title("Recoveries")
        ax3.plot(new_cases["Active Cases"], 'g-')
        ax3.set_title("Active Cases")
        ax3.set_xticks(range(len(new_cases.index)))
        ax3.set_xticklabels(new_cases.index, rotation=75)
        plt.figure(figsize=(10, 5))
        plt.plot(new_cases["New Cases"], 'b--', label="New Cases")
        plt.plot(new_cases["Recoveries"], 'r--', label="Recoveries")
        plt.plot(new_cases["Active Cases"], 'g-', label="Active Cases")
        plt.title("Covid 19 in NZ")
        plt.xticks(range(len(new_cases.index)), new_cases.index, rotation=75)
        plt.legend(loc='best')
        plt.tight_layout()
        plt.show()

    plot_active_cases(r"C:\Users\johns\Desktop\Random Python Projects\reoveries until april 9.csv", new_cases_per_date)

 # TODO refactor to isolate sections of the code to work independently
if __name__ == "__main__":
    covid_plotting()
