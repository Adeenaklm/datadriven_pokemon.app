class Pokemon:
    def __init__(self, name, types, stats, abilities, image_url):
        self.name = name
        self.types = types
        self.stats = stats
        self.abilities = abilities
        self.image_url = image_url

    def get_stat(self, stat_name):
        return self.stats.get(stat_name, "N/A")
