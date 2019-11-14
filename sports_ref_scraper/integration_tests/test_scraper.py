import unittest

import requests
from bs4 import BeautifulSoup

from sports_ref_scraper.parsing import extract_table, find_table


class TestAsExpected(unittest.TestCase):

    def test_scraping(self):
        # This page should not be updated with new data as of this writing
        # The only changes that would occur would be structural
        url = "https://www.basketball-reference.com/leagues/NBA_2019_advanced.html"
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        table_str = find_table(soup, 'advanced_stats')
        table_data = extract_table(table_str, header_row=0, start_of_rows=1)
        self.assertEqual((734, 29), table_data.shape)
