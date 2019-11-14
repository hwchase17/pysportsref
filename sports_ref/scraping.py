import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from .parsing import extract_table, find_table


def get_year_stats(url_formatter, year, table_name):
    """Get html for page for given year, find and extract table, add year column."""
    url = url_formatter.format(year=year)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features="html.parser")
    table_tag = find_table(soup, table_name)
    table_data = extract_table(table_tag, get_url=True)
    table_data['year'] = year
    return table_data


def get_stats_for_years(url_formatter, start_year, end_year, table_name):
    """Get table data from url for range of years."""
    all_dfs = []
    for year in tqdm(range(start_year, end_year)):
        all_dfs.append(get_year_stats(url_formatter, year, table_name))
    return pd.concat(all_dfs).reset_index(drop=True)
