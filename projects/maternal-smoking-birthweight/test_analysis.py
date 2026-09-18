"""Keep missing exposure status separate from nonsmoking."""

import unittest
import numpy as np
import pandas as pd
from analysis import encode_smoking


class ExposureChecks(unittest.TestCase):
    def test_missing_exposure_remains_missing(self):
        result = encode_smoking(pd.Series([0.0, 1.0, 2.0, 3.0, np.nan]))
        np.testing.assert_allclose(result[:4], [0, 1, 1, 1])
        self.assertTrue(pd.isna(result.iloc[4]))

    def test_unknown_codes_fail(self):
        with self.assertRaises(ValueError):
            encode_smoking(pd.Series([0, 99]))


if __name__ == "__main__":
    unittest.main()
