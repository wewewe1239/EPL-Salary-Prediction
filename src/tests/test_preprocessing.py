import unittest
import pandas as pd
from preprocessing import normalize_names, match_players_with_different_names
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


    def test_match_players_with_different_names_should_replace_make_same_players_have_same_names(self):
        input_df_stats = pd.DataFrame(
            {
                "Name": [
                    "pedro",
                    "fred",
                    "fred",
                    "son heung min"
                ],
                "Team": [
                    "CFC",
                    "MUFC",
                    "MUFC",
                    "THFC"
                ]
            }
        )

        input_df_salaries = pd.DataFrame(
            {
                "Name": [
                    "pedro rodriguez",
                    "frederico de paula pantos",
                    "freddie woodman",
                    "heung min son"
                ],
                "Team": [
                    "CFC",
                    "MUFC",
                    "NUFC",
                    "THFC"
                ]
            }
        )

        actual_df = match_players_with_different_names(input_df_stats, input_df_salaries)

        expected_df = pd.DataFrame(
            {
                "Name": [
                    "pedro rodriguez",
                    "frederico de paula pantos",
                    "frederico de paula pantos",
                    "heung min son"
                ],
                "Team": [
                    "CFC",
                    "MUFC",
                    "MUFC",
                    "THFC"
                ]
            }
        )

        assert_frame_equal(actual_df, expected_df)


