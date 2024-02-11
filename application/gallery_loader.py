import json
import logging
from datetime import timedelta
from typing import List, TYPE_CHECKING

import redis

from application.gallery_image import GalleryImage

if TYPE_CHECKING:
    from application import GithubClient


LOG = logging.getLogger(__name__)
BOOK_GALLERY_API_ROOT = "https://api.github.com/repos/Tyler-Yates/historical-objects-static/contents/images/books"
MEDAL_GALLERY_API_ROOT = "https://api.github.com/repos/Tyler-Yates/historical-objects-static/contents/images/medals"

CACHE_TTL = timedelta(days=30)


class GalleryLoader:
    def __init__(self, redis_client: redis.client.Redis, github_client: "GithubClient"):
        self.redis_client = redis_client
        self.github_client = github_client

    def load_medal_gallery_images(
        self,
        medal_id: str,
    ) -> List[GalleryImage]:
        gallery = []
        request_url = f"{MEDAL_GALLERY_API_ROOT}/{medal_id}/hi"

        # Try to load the value from cache
        gallery_files_json_string = self.redis_client.get(request_url)

        # If there is no cache value, make a request to get the actual value
        if gallery_files_json_string is None:
            # Make a request to the actual URL
            response = self.github_client.make_request(request_url)
            response.raise_for_status()

            # Add the value to the cache
            self.redis_client.set(request_url, response.text, ex=CACHE_TTL)

            # Use the response
            gallery_files_json_string = response.text

        # Parse the gallery files
        json_data = json.loads(gallery_files_json_string)
        for item in json_data:
            item_name: str = item["path"].split("/")[-1]

            # Skip over the expected images
            if item_name.startswith(f"{medal_id}_obverse.") or item_name.startswith(f"{medal_id}_reverse."):
                continue

            gallery.append(GalleryImage(item["download_url"].replace("/hi/", "/low/"), item["download_url"]))

        return gallery

    def load_book_gallery_images(self, book_id: str) -> List[GalleryImage]:
        gallery = []
        request_url = f"{BOOK_GALLERY_API_ROOT}/{book_id}/gallery/hi"

        # Try to load the value from cache
        gallery_files_json_string = self.redis_client.get(request_url)

        # If there is no cache value, make a request to get the actual value
        if gallery_files_json_string is None:
            # Make a request to the actual URL
            response = self.github_client.make_request(request_url)
            response.raise_for_status()

            # Add the value to the cache
            self.redis_client.set(request_url, response.text, ex=CACHE_TTL)

            # Use the response
            gallery_files_json_string = response.text

        # Parse the gallery files
        json_data = json.loads(gallery_files_json_string)
        for item in json_data:
            gallery.append(
                GalleryImage(item["download_url"].replace("/gallery/hi", "/gallery/low"), item["download_url"])
            )

        return gallery
