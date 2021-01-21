import collections
import json
import logging
import os
from typing import List

import requests

from book import Book
from gallery_image import GalleryImage
from medal import Medal
from plate import Plate

LOG = logging.getLogger(__name__)
BOOK_GALLERY_API_ROOT = "https://api.github.com/repos/Tyler-Yates/historical-objects-static/contents/images/books"


def _load_medals_data(application):
    data_path = os.path.join(application.static_folder, "data", "medals")
    for json_file_name in os.listdir(data_path):
        object_id = json_file_name.replace('.json', '')
        with open(os.path.join(data_path, json_file_name), encoding="utf8", mode='r') as json_file:
            json_data = json.load(json_file, object_pairs_hook=collections.OrderedDict)

            # Try using the simple year field first for sorting
            sort_year = -1
            try:
                sort_year = int(json_data.get('year', None))
            except Exception:
                pass
            # If that does not work, fall back to the sort_year field
            try:
                sort_year = int(json_data.get('sort_year', None))
            except Exception:
                pass
            # Log if we could not find a sortable year
            if sort_year == -1:
                LOG.warning("No sort year for {}".format(json_file_name))

            medal = Medal(id=object_id,
                          name=json_data.get('name', None),
                          engraver=json_data.get('engraver', None),
                          year=json_data.get('year', None),
                          country=json_data.get('country', None),
                          diameter=json_data.get('diameter', None),
                          obverse_description=json_data.get('obverse', None),
                          obverse_inscriptions=json_data.get('obverse_inscriptions', []),
                          reverse_description=json_data.get('reverse', None),
                          reverse_inscriptions=json_data.get('reverse_inscriptions', []),
                          references=json_data.get('references', None),
                          history=json_data.get('description', None),
                          sort_year=sort_year)

            application.medals[object_id] = medal

    # Sort by year
    application.medals = collections.OrderedDict(sorted(application.medals.items(), key=lambda x: x[1].sort_year))


def _load_gallery_images(book_id: str) -> List[GalleryImage]:
    gallery = []
    request_url = f"{BOOK_GALLERY_API_ROOT}/{book_id}/gallery/hi"
    response = requests.get(request_url)
    response.raise_for_status()

    json_data = json.loads(response.text)
    for item in json_data:
        gallery.append(GalleryImage(
            item["download_url"].replace("/gallery/hi", "/gallery/low"),
            item["download_url"]
        ))

    return gallery


def _load_books_data(application):
    data_path = os.path.join(application.static_folder, "data", "books")
    for json_file_name in os.listdir(data_path):
        object_id = json_file_name.replace('.json', '')
        with open(os.path.join(data_path, json_file_name), encoding="utf8", mode='r') as json_file:
            json_data = json.load(json_file, object_pairs_hook=collections.OrderedDict)

            # Try using the simple year field first for sorting
            sort_year = -1
            try:
                sort_year = int(json_data.get('year', None))
            except Exception:
                pass
            # If that does not work, fall back to the sort_year field
            try:
                sort_year = int(json_data.get('sort_year', None))
            except Exception:
                pass
            # Log if we could not find a sortable year
            if sort_year == -1:
                LOG.warning("No sort year for {}".format(json_file_name))

            gallery_images = []
            try:
                gallery_images = _load_gallery_images(object_id)
            except Exception as e:
                print(f"Error loading gallery for {object_id}: {e}")

            book = Book(id=object_id,
                        title=json_data.get('title', None),
                        author=json_data.get('author', None),
                        year=json_data.get('year', None),
                        size=json_data.get('size', None),
                        oclc=json_data.get('oclc', None),
                        history=json_data.get('description', None),
                        sort_year=sort_year,
                        gallery_images=gallery_images)

            application.books[object_id] = book

    # Sort by year
    application.books = collections.OrderedDict(sorted(application.books.items(), key=lambda x: x[1].sort_year))


def _load_plates_data(application):
    data_path = os.path.join(application.static_folder, "data", "plates")
    for json_file_name in os.listdir(data_path):
        object_id = json_file_name.replace('.json', '')
        with open(os.path.join(data_path, json_file_name), encoding="utf8", mode='r') as json_file:
            json_data = json.load(json_file, object_pairs_hook=collections.OrderedDict)

            # Try using the simple year field first for sorting
            sort_year = -1
            try:
                sort_year = int(json_data.get('year', None))
            except Exception:
                pass
            # If that does not work, fall back to the sort_year field
            try:
                sort_year = int(json_data.get('sort_year', None))
            except Exception:
                pass
            # Log if we could not find a sortable year
            if sort_year == -1:
                LOG.warning("No sort year for {}".format(json_file_name))

            plate = Plate(id=object_id,
                          title=json_data.get('title', None),
                          artist=json_data.get('artist', None),
                          year=json_data.get('year', None),
                          sort_year=sort_year)

            application.plates[object_id] = plate

    # Sort by year
    application.plates = collections.OrderedDict(sorted(application.plates.items(), key=lambda x: x[1].sort_year))


def load_data(application):
    _load_medals_data(application)
    _load_books_data(application)
    _load_plates_data(application)


def migrate_old_data(application):
    # Migrate old medals data
    json_file_path = os.path.join(application.static_folder, "json", "medals.json")
    with open(json_file_path, encoding="utf8", mode='r') as json_file:
        json_data = json.load(json_file, object_pairs_hook=collections.OrderedDict)['medals']
        for entry_id in json_data:
            with open(os.path.join(application.static_folder, "data", "medals", "{}.json".format(entry_id)),
                      encoding="utf8", mode='w') as outfile:
                json.dump(json_data[entry_id], outfile, indent=4)

    # Migrate old books data
    json_file_path = os.path.join(application.static_folder, "json", "books.json")
    with open(json_file_path, encoding="utf8", mode='r') as json_file:
        json_data = json.load(json_file, object_pairs_hook=collections.OrderedDict)['books']
        for entry_id in json_data:
            with open(os.path.join(application.static_folder, "data", "books", "{}.json".format(entry_id)),
                      encoding="utf8", mode='w') as outfile:
                json.dump(json_data[entry_id], outfile, indent=4)

    # Migrate old plates data
    json_file_path = os.path.join(application.static_folder, "json", "plates.json")
    with open(json_file_path, encoding="utf8", mode='r') as json_file:
        json_data = json.load(json_file, object_pairs_hook=collections.OrderedDict)['plates']
        for entry_id in json_data:
            with open(os.path.join(application.static_folder, "data", "plates", "{}.json".format(entry_id)),
                      encoding="utf8", mode='w') as outfile:
                json.dump(json_data[entry_id], outfile, indent=4)
