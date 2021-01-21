from typing import List

from gallery_image import GalleryImage


class Book:
    def __init__(self, id, title, author, year, size, oclc, history, sort_year, gallery_images: List[GalleryImage]):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.size = size
        self.oclc = oclc
        self.history = history
        self.sort_year = sort_year
        self.gallery_images = gallery_images
