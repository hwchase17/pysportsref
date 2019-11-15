import unittest

import requests
from bs4 import BeautifulSoup

from ..parsing import get_table_from_soup, get_table_soup


class TestAsExpected(unittest.TestCase):

    def test_scraping(self):
        # This page should not be updated with new data as of this writing
        # The only changes that would occur would be structural
        url = "https://www.basketball-reference.com/leagues/NBA_2019_advanced.html"
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        table_str = get_table_soup(soup, 'advanced_stats')
        table_data = get_table_from_soup(table_str)
        self.assertEqual((530, 29), table_data.shape)
