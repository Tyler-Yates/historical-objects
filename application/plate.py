class Plate:
    def __init__(self, id, title, artist, year, sort_year, description):
        self.id = id
        self.title = title
        self.artist = artist
        self.year = year
        self.sort_year = sort_year
        self.description = " ".join(description) if description else None
