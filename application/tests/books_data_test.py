import json
import os
from typing import List, Dict

import pytest

CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
BOOKS_DATA_PATH = os.path.realpath(os.path.join(CURRENT_FILE_PATH, "..", "static", "data", "books"))

EXPECTED_KEYS = frozenset(
    [
        "title",
        "year",
        "author",
        "size",
        "oclc",
    ]
)

NON_EMPTY_KEYS = frozenset(["title", "year", "author", "size", "oclc"])


class TestData:
    @staticmethod
    def _get_book_files() -> List[str]:
        files = []

        for book_file_name in os.listdir(BOOKS_DATA_PATH):
            if not book_file_name.endswith(".json"):
                continue
            files.append(book_file_name)

        files.sort()
        return files

    @pytest.mark.parametrize("book_file_name", _get_book_files())
    def test_medal_data(self, book_file_name):
        with open(os.path.join(BOOKS_DATA_PATH, book_file_name), mode="r") as medal_file:
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
