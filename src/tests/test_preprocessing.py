import unittest
import pandas as pd
from preprocessing import normalize_names
from pandas.testing import assert_frame_equal


class TestFunctionnal(unittest.TestCase):
    def test_normalize_names_should_remove_uniform_names_and_remove_extras(self):
        input_df = pd.DataFrame(
            {
                "Name": [
                    "David de Gea",
                    "Alexis Sànchez",
                    "Danny Ings (on loan from )",
                    "Ki Sung-yueng"
                ]
            }
        )

        actual_df = normalize_names(input_df)

        expected_df = pd.DataFrame(
            {
                "Name": [
                    "david de gea",
                    "alexis sanchez",
                    "danny ings",
                    "ki sung yueng"
                ]
            }
        )

        assert_frame_equal(actual_df, expected_df)

    

