class Medal:
    def __init__(self, id, name, engraver, year, country, diameter, obverse_description, obverse_inscriptions,
                 reverse_description, reverse_inscriptions, references, history, sort_year):
        self.id = id
        self.name = name
        self.engraver = engraver
        self.year = year
        self.country = country
        self.diameter = diameter
        self.obverse_description = obverse_description
        self.obverse_inscriptions = obverse_inscriptions
        self.reverse_description = reverse_description
        self.reverse_inscriptions = reverse_inscriptions
        self.references = references
        self.history = ' '.join(history)
        self.sort_year = sort_year
