from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

world_data = pd.read_html("https://en.wikipedia.org/wiki/Template:2019%E2%80%9320_coronavirus_pandemic_data", header=0)
world_data = world_data[0]
world_data.drop(0, inplace=True)
world_data.drop([224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235], inplace=True)
world_data.drop('Countries and territories[a]', axis =1, inplace=True)
world_data = world_data.iloc[:, 0:4]
world_data.rename(columns = {'Countries and territories[a].1':"Countries", "Cases[b]":"Cases", 'Deaths[c]':"Deaths",
                             "Recov.[d]":"Recovered"}, inplace=True)
world_data["Recovered"].replace("–", '0', inplace=True)
world_data["Cases"] = pd.to_numeric(world_data["Cases"])
world_data["Deaths"] = pd.to_numeric(world_data["Deaths"])
world_data["Recovered"] = pd.to_numeric(world_data["Recovered"])
world_data['Mortality rate (%)'] = world_data["Deaths"]/world_data['Cases']*100
world_data["Cases Rank"] = world_data.index +1
world_data.sort_values(by="Deaths", ascending=False, inplace=True)
world_data.reset_index(drop = True, inplace=True)
world_data["Death rank"] = world_data.index +1
world_data.sort_values(by='Mortality rate (%)', ascending=False, inplace=True)
world_data.reset_index(drop=True, inplace=True)
world_data['Mortality Rank'] = world_data.index +1
world_data.sort_values(by="Cases", ascending=False, inplace=True)
world_data.reset_index(drop=True, inplace=True)

def covid_search(Country):
    series = world_data[world_data["Countries"] == Country]
    print(series)

covid_search("New Zealand")
covid_search("Australia[x]")

# TODO fix search "country' labels include [x] for some reason, maybe use regex or .replace()