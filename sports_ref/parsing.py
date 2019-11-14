import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


def _clean_soup(soup):
    """Clean up html to get rid of tricky comments."""
    return BeautifulSoup(str(soup).replace('<!--', '').replace('-->', ''))


def get_urls(row):
    """Get urls for all cells in table row."""
    all = row.findAll('th') + row.findAll('td')
    return [t.find('a')['href'] if t.find('a') else np.nan for t in all]


def list_tables(soup):
    """List tables present in BSoup object that we know how to fetch."""
    soup = _clean_soup(soup)
    return [t.attrs['id'] for t in soup.findAll('table') if 'id' in t.attrs]


def extract_table(table_str, header_row=0, start_of_rows=1, get_url=False):
    """Extract table from html to pd.DataFrame."""
    columns = [t['data-stat'] for t in table_str.findAll('tr')[header_row].findAll('th')]
    rows = [
        [r.find('th').text] + [t.text for t in r.findAll('td')]
        for r in table_str.findAll('tr')[start_of_rows:]
    ]
    df = pd.DataFrame(rows, columns=columns)
    if get_url:
        extra_rows = [get_urls(r) for r in table_str.findAll('tr')[start_of_rows:]]
        extra_df = pd.DataFrame(extra_rows, columns=[c + '_url' for c in columns])
        non_empty_cols = extra_df.notnull().sum()[lambda x: x != 0].index
        df = pd.concat([df, extra_df[non_empty_cols]], axis=1)
    return df


def find_table(soup, table_name):
    """Find html for table, even if in a comment."""
    soup = _clean_soup(soup)
    tables = soup.findAll('table', {"id": table_name})
    if tables:
        return tables[0]
    else:
        raise ValueError('table {} not found'.format(table_name))
