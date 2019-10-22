class ItemDetails:

    def __init__(self, item_id, competition, name_author, datentime, overview, comments, votes):
        # (self, item_id, title, overview, comments):
        self.comments = comments
        self.overview = overview
        self.item_id = item_id
        self.competition = competition
        self.name_author = name_author
        self.votes = votes
        self.datentime = datentime

    def description(self):
        return "".join([self.overview, self.comments])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__ + " ID: " + str(self.item_id)
