import unittest

import numpy as np
import pandas as pd

from ..data import filter_df, merge_with_prev_year


class TestData(unittest.TestCase):

    def test_filter_df(self):
        mock_df = pd.DataFrame(
            [
                ['harry', 2018, 'kensho', 1],
                ['harry', 2019, 'kensho', 2],
                ['harry', 2019, 'TOT', 3],
                ['harry', 2019, 'ri', 4],
                ['hallas', 2018, 'harvard', 5],
                ['hallas', 2019, 'harvard', 6],
            ],
            columns=['name', 'year', 'team_id', 'var1']
        )

        expected_df = pd.DataFrame(
            [
                ['harry', 2018, 'kensho', 1],
                ['harry', 2019, 'TOT', 3],
                ['hallas', 2018, 'harvard', 5],
                ['hallas', 2019, 'harvard', 6],
            ],
            columns=['name', 'year', 'team_id', 'var1']
        )

        output_df = filter_df(mock_df, player_col='name')
        pd.testing.assert_frame_equal(expected_df, output_df)

        with self.assertRaises(ValueError):
            filter_df(mock_df)

        # Test with no values of 'TOT'
        mock_df = pd.DataFrame(
            [
                ['harry', 2018, 'kensho', 1],
            ], columns=['name', 'year', 'team_id', 'var1']
        )

        expected_df = pd.DataFrame(
            [
                ['harry', 2018, 'kensho', 1],
            ], columns=['name', 'year', 'team_id', 'var1']
        )
        output_df = filter_df(mock_df, player_col='name')
        pd.testing.assert_frame_equal(expected_df, output_df)

    def test_merge_with_prev_year(self):
        mock_df = pd.DataFrame(
            [
                ['harry', 2018, 'kensho', 1],
                ['harry', 2019, 'TOT', 3],
                ['hallas', 2017, 'harvard', 3],
                ['hallas', 2018, 'harvard', 5],
                ['hallas', 2019, 'harvard', 6],
            ],
            columns=['player_url', 'year_col', 'team_id', 'var1']
        )

        expected_df = pd.DataFrame(
            [
                ['harry', 2018, 'kensho', 1, np.nan, np.nan],
                ['harry', 2019, 'TOT', 3, 'kensho', 1],
                ['hallas', 2017, 'harvard', 3, np.nan, np.nan],
                ['hallas', 2018, 'harvard', 5, 'harvard', 3],
                ['hallas', 2019, 'harvard', 6, 'harvard', 5],
            ],
            columns=['player_url', 'year_col', 'team_id', 'var1', 'team_id___1', 'var1___1']
        )

        output_df = merge_with_prev_year(mock_df, 1, year_col='year_col')
        pd.testing.assert_frame_equal(expected_df, output_df)

        expected_df = pd.DataFrame(
            [
                ['harry', 2018, 'kensho', 1, np.nan, np.nan],
                ['harry', 2019, 'TOT', 3, np.nan, np.nan],
                ['hallas', 2017, 'harvard', 3, np.nan, np.nan],
                ['hallas', 2018, 'harvard', 5, np.nan, np.nan],
                ['hallas', 2019, 'harvard', 6, 'harvard', 3],
            ],
            columns=['player_url', 'year_col', 'team_id', 'var1', 'team_id___2', 'var1___2']
        )

        output_df = merge_with_prev_year(mock_df, 2, year_col='year_col')
        pd.testing.assert_frame_equal(expected_df, output_df)
