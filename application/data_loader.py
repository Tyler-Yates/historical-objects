import collections
import json
import logging
import os
from typing import Dict

from .book import Book
from .medal import Medal
from .plate import Plate

LOG = logging.getLogger(__name__)
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


def _load_medals_data():
    medals = {}

    data_path = os.path.join(ROOT_PATH, "static", "data", "medals")
    for json_file_name in os.listdir(data_path):
        object_id = json_file_name.replace(".json", "")
        with open(os.path.join(data_path, json_file_name), encoding="utf8", mode="r") as json_file:
            json_data = json.load(json_file, object_pairs_hook=collections.OrderedDict)

            # Try using the simple year field first for sorting
            sort_year = -1
            try:
                sort_year = int(json_data.get("year", None))
            except Exception:
                pass
            # If that does not work, fall back to the sort_year field
            try:
                sort_year = int(json_data.get("sort_year", None))
            except Exception:
                pass
            # Log if we could not find a sortable year
            if sort_year == -1:
                LOG.warning("No sort year for {}".format(json_file_name))

            medal = Medal(
                medal_id=object_id,
                name=json_data.get("name", None),
                engraver=json_data.get("engraver", None),
                year=json_data.get("year", None),
                country=json_data.get("country", None),
                diameter=json_data.get("diameter", None),
                obverse_description=json_data.get("obverse", None),
                obverse_inscriptions=json_data.get("obverse_inscriptions", []),
                reverse_description=json_data.get("reverse", None),
                reverse_inscriptions=json_data.get("reverse_inscriptions", []),
                references=json_data.get("references", None),
                history=json_data.get("description", None),
                sort_year=sort_year,
            )

            medals[object_id] = medal

    # Sort by year
    return collections.OrderedDict(sorted(medals.items(), key=lambda x: x[1].sort_year))


def _load_books_data():
    books = {}

    data_path = os.path.join(ROOT_PATH, "static", "data", "books")
    for json_file_name in os.listdir(data_path):
        object_id = json_file_name.replace(".json", "")
        with open(os.path.join(data_path, json_file_name), encoding="utf8", mode="r") as json_file:
            json_data = json.load(json_file, object_pairs_hook=collections.OrderedDict)

            # Try using the simple year field first for sorting
            sort_year = -1
            try:
                sort_year = int(json_data.get("year", None))
            except Exception:
                pass
            # If that does not work, fall back to the sort_year field
            try:
                sort_year = int(json_data.get("sort_year", None))
            except Exception:
                pass
            # Log if we could not find a sortable year
            if sort_year == -1:
                LOG.warning("No sort year for {}".format(json_file_name))

            book = Book(
                id=object_id,
                title=json_data.get("title", None),
                author=json_data.get("author", None),
                year=json_data.get("year", None),
                size=json_data.get("size", None),
                oclc=json_data.get("oclc", None),
                history=json_data.get("description", None),
                sort_year=sort_year,
            )

            books[object_id] = book

    # Sort by year
    return collections.OrderedDict(sorted(books.items(), key=lambda x: x[1].sort_year))


def _load_plates_data():
    plates = {}

    data_path = os.path.join(ROOT_PATH, "static", "data", "plates")
    for json_file_name in os.listdir(data_path):
        object_id = json_file_name.replace(".json", "")
        with open(os.path.join(data_path, json_file_name), encoding="utf8", mode="r") as json_file:
            json_data = json.load(json_file, object_pairs_hook=collections.OrderedDict)

            # Try using the simple year field first for sorting
            sort_year = -1
            try:
                sort_year = int(json_data.get("year", None))
            except Exception:
                pass
            # If that does not work, fall back to the sort_year field
            try:
                sort_year = int(json_data.get("sort_year", None))
            except Exception:
                pass
            # Log if we could not find a sortable year
            if sort_year == -1:
                LOG.warning("No sort year for {}".format(json_file_name))

            plate = Plate(
                id=object_id,
                title=json_data.get("title", None),
                artist=json_data.get("artist", None),
                year=json_data.get("year", None),
                sort_year=sort_year,
                description=json_data.get("description", None),
            )

            plates[object_id] = plate

    # Sort by year
    return collections.OrderedDict(sorted(plates.items(), key=lambda x: x[1].sort_year))


def load_data() -> Dict[str, Dict]:
    return {
        "medals": _load_medals_data(),
        "books": _load_books_data(),
        "plates": _load_plates_data(),
    }


def migrate_old_data(application):
    # Migrate old medals data
    json_file_path = os.path.join(application.static_folder, "json", "medals.json")
    with open(json_file_path, encoding="utf8", mode="r") as json_file:
        json_data = json.load(json_file, object_pairs_hook=collections.OrderedDict)["medals"]
        for entry_id in json_data:
            with open(
                os.path.join(application.static_folder, "data", "medals", "{}.json".format(entry_id)),
                encoding="utf8",
                mode="w",
            ) as outfile:
                json.dump(json_data[entry_id], outfile, indent=4)

    # Migrate old books data
    json_file_path = os.path.join(application.static_folder, "json", "books.json")
    with open(json_file_path, encoding="utf8", mode="r") as json_file:
        json_data = json.load(json_file, object_pairs_hook=collections.OrderedDict)["books"]
        for entry_id in json_data:
            with open(
                os.path.join(application.static_folder, "data", "books", "{}.json".format(entry_id)),
                encoding="utf8",
                mode="w",
            ) as outfile:
                json.dump(json_data[entry_id], outfile, indent=4)

    # Migrate old plates data
    json_file_path = os.path.join(application.static_folder, "json", "plates.json")
    with open(json_file_path, encoding="utf8", mode="r") as json_file:
        json_data = json.load(json_file, object_pairs_hook=collections.OrderedDict)["plates"]
        for entry_id in json_data:
            with open(
                os.path.join(application.static_folder, "data", "plates", "{}.json".format(entry_id)),
                encoding="utf8",
                mode="w",
            ) as outfile:
                json.dump(json_data[entry_id], outfile, indent=4)
