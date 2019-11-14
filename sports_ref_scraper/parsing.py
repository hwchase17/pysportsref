import numpy as np
import pandas as pd
from bs4 import BeautifulSoup, Comment


def get_urls(row):
    """Get urls for all cells in table row."""
    all = row.findAll('th') + row.findAll('td')
    return [t.find('a')['href'] if t.find('a') else np.nan for t in all]


def list_tables(soup):
    """List tables present in BSoup object that we know how to fetch."""
    table_names = [t.attrs['id'] for t in soup.findAll('table')]
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        if '<table' in comment:
            tables = BeautifulSoup(comment, "lxml").findAll('table')
            for table in tables:
                if 'id' in table.attrs:
                    table_names.append(table.attrs['id'])
    return table_names


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
    tables = soup.findAll('table', {"id": table_name})
    if tables:
        return tables[0]
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))
    table_comment = next(c for c in comments if 'id="{}"'.format(table_name) in c)
    table_soup = BeautifulSoup(table_comment, "lxml")
    return table_soup.findAll('table', {"id": table_name})[0]
