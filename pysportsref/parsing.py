import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


def _clean_soup(soup):
    """Clean up html to get rid of tricky comments."""
    return BeautifulSoup(str(soup).replace('<!--', '').replace('-->', ''), "lxml")


def _get_urls(row):
    """Get urls for all cells in table row."""
    all = row.findAll('th') + row.findAll('td')
    return [t.find('a')['href'] if t.find('a') else np.nan for t in all]


def list_tables(soup):
    """List tables present in BSoup object that we know how to fetch."""
    soup = _clean_soup(soup)
    return [t.attrs['id'] for t in soup.findAll('table') if 'id' in t.attrs]


def _convert_dtypes(df):
    """Convert dtypes of df, when possible."""
    for col in df.columns:
        try:
            df[col] = [int(i) if i != '' and i is not None else None for i in df[col]]
        except ValueError:
            try:
                df[col] = df[col].replace('', np.nan).astype(float)
            except ValueError:
                pass
    return df


def get_table_from_soup(table_soup, get_url=False, include_tfoot=False):
    """Extract table from html to pd.DataFrame."""
    th_soups = table_soup.find('thead').findAll('tr')
    columns = [t['data-stat'] for t in th_soups[-1].findAll('th')]
    row_soups = table_soup.findAll('tr', {'class': 'full_table'})
    if not row_soups:
        row_soups = table_soup.find('tbody').findAll('tr')
    if include_tfoot:
        row_soups.extend(table_soup.find('tfoot').findAll('tr'))
    rows = [[r.find('th').text] + [t.text for t in r.findAll('td')] for r in row_soups]
    df = pd.DataFrame(rows, columns=columns)
    if get_url:
        extra_rows = [_get_urls(r) for r in row_soups]
        extra_df = pd.DataFrame(extra_rows, columns=[c + '_url' for c in columns])
        non_empty_cols = extra_df.notnull().sum()[lambda x: x != 0].index
        df = pd.concat([df, extra_df[non_empty_cols]], axis=1)
    return _convert_dtypes(df)


def get_table_soup(soup, table_name):
    """Find html for table, even if in a comment."""
    soup = _clean_soup(soup)
    tables = soup.findAll('table', {"id": table_name})
    if tables:
        return tables[0]
    else:
        raise ValueError('table {} not found'.format(table_name))
