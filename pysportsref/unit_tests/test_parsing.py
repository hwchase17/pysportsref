import os
import unittest

import pandas as pd
from bs4 import BeautifulSoup

from ..parsing import get_table_from_soup, get_table_soup, list_tables

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


class TestParsing(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open(os.path.join(data_path, 'mock_page.txt')) as f:
            content = f.read()
        cls.soup = BeautifulSoup(content, "lxml")
        with open(os.path.join(data_path, 'mock_table.txt')) as f:
            cls.expected_base_tag = BeautifulSoup(f.read(), "lxml").find('table')
        with open(os.path.join(data_path, 'mock_table_in_comments.txt')) as f:
            cls.expected_comment_tag = BeautifulSoup(f.read(), "lxml").find('table')

    def test_get_table_soup(self):
        # Test with regular table
        table_tag = get_table_soup(self.soup, 'confs_standings_E')
        self.assertEqual(self.expected_base_tag, table_tag)

        # Test with table in comments
        table_tag = get_table_soup(self.soup, 'misc_stats')
        self.assertEqual(self.expected_comment_tag, table_tag)

    def test_get_table_from_soup(self):
        # Test with normal table
        table_data = get_table_from_soup(self.expected_base_tag)
        expected_df = pd.read_csv(os.path.join(data_path, 'mock_data.csv'), dtype=str)
        pd.testing.assert_frame_equal(expected_df.drop('team_name_url', axis=1), table_data)

        # Test getting urls
        table_data = get_table_from_soup(self.expected_base_tag, get_url=True)
        pd.testing.assert_frame_equal(expected_df, table_data)

        # Test with headers on second row
        expected_df = pd.read_csv(os.path.join(data_path, 'mock_data_multiheader.csv'), dtype=str)
        expected_df = expected_df.fillna('')
        table_data = get_table_from_soup(self.expected_comment_tag, include_tfoot=True)
        pd.testing.assert_frame_equal(expected_df, table_data)

        # Test without tfoot
        table_data = get_table_from_soup(self.expected_comment_tag)
        pd.testing.assert_frame_equal(expected_df.iloc[:-1], table_data)

    def test_list_tables(self):
        expected_result = [
            'confs_standings_E',
            'confs_standings_W',
            'divs_standings_E',
            'divs_standings_W',
            'all_playoffs',
            'team-stats-per_game',
            'opponent-stats-per_game',
            'team-stats-base',
            'opponent-stats-base',
            'team-stats-per_poss',
            'opponent-stats-per_poss',
            'misc_stats',
            'team_shooting',
            'opponent_shooting',
            'all_awards',
        ]
        found_tables = list_tables(self.soup)
        self.assertListEqual(expected_result, found_tables)
