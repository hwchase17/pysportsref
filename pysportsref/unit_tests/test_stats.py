import unittest

import numpy as np
import pandas as pd

from ..stats import calculate_aging_curve


class TestStats(unittest.TestCase):

    def test_calculate_aging_curve(self):
        mock_df = pd.DataFrame(
            [
                [np.nan, 4., 2., 6., 19],
                [2., 1., 1., 3., 20],
                [2., 4., 2., 6., 20],
                [1., 4., 2., 6., 21],
                [3., np.nan, 2., 6., 21],
            ],
            columns=['col', 'col___1', 'mp', 'mp___1', 'age']
        )
        output_series = calculate_aging_curve(mock_df, 'col', 'mp')
        m1 = 2 / (1 / 1 + 1 / 3)
        m2 = 2 / (1 / 2 + 1 / 6)
        expected_series = pd.Series(
            [
                0.,  # fillna to 0
                (1. * m1 + -2 * m2) / (m1 + m2),
                -4,  # cumulative sum
            ],
            index=pd.Index([19, 20, 21], name='age')
        )
        pd.testing.assert_series_equal(expected_series, output_series)
