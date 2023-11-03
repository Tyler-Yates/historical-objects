import json
import os
from typing import List, Dict

import pytest

CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
MEDALS_DATA_PATH = os.path.realpath(os.path.join(CURRENT_FILE_PATH, "..", "static", "data", "medals"))

EXPECTED_KEYS = frozenset(
    [
        "name",
        "engraver",
        "country",
        "year",
        "diameter",
        "obverse",
        "obverse_inscriptions",
        "reverse",
        "reverse_inscriptions",
        "references",
        "description",
    ]
)

NON_EMPTY_KEYS = frozenset(["name", "year", "diameter"])


class TestData:
    @staticmethod
    def _get_medal_files() -> List[str]:
        files = []

        for medal_file_name in os.listdir(MEDALS_DATA_PATH):
            if not medal_file_name.endswith(".json"):
                continue
            files.append(medal_file_name)

        files.sort()
        return files

    @pytest.mark.parametrize("medal_file_name", _get_medal_files())
    def test_medal_data(self, medal_file_name):
        with open(os.path.join(MEDALS_DATA_PATH, medal_file_name), mode="r") as medal_file:
            json_data: Dict = json.load(medal_file)

            # Assert that every key we expect is present
            for key in EXPECTED_KEYS:
                assert key in json_data

            # Assert that some keys are non-empty
            unexpectedly_empty_keys = []
            for key in NON_EMPTY_KEYS:
                if not json_data[key]:
                    unexpectedly_empty_keys.append(key)

            assert unexpectedly_empty_keys == [], f"The following keys are empty: {unexpectedly_empty_keys}"
