import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from .parsing import get_table_from_soup, get_table_soup


def get_soup(url):
    """Get beautiful soup representation of a url."""
    r = requests.get(url)
    return BeautifulSoup(r.content, features="html.parser")


def get_stats_for_year(url_formatter, year, table_name):
    """Get html for page for given year, find and extract table, add year column."""
    url = url_formatter.format(year=year)
    soup = get_soup(url)
    table_tag = get_table_soup(soup, table_name)
    table_data = get_table_from_soup(table_tag, get_url=True)
    table_data['year'] = year
    return table_data


def get_stats_for_years(url_formatter, start_year, end_year, table_name):
    """Get table data from url for range of years."""
    all_dfs = []
    for year in tqdm(range(start_year, end_year + 1)):
        all_dfs.append(get_stats_for_year(url_formatter, year, table_name))
    return pd.concat(all_dfs, sort=True).reset_index(drop=True)
