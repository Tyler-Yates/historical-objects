class Book:
    def __init__(self, id, title, author, year, size, oclc, history, sort_year):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.size = size
        self.oclc = oclc
        self.history = " ".join(history) if history else None
        self.sort_year = sort_year
