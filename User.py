class User:
    def __init__(self, name, level, inventory, race):
        self.name = name
        self.level = level
        self.inventory = inventory
        self.race = race

    def __repr__(self) -> str:
        pass

    def add_to_inventory(self, item):
        pass

    def remove_from_inventory(self, item):
        pass

    def display_inventory(self):        
        print(f"{self.name}'s inventory: {', '.join(self.inventory)}")

    def display_level(self):
        print(f"{self.name}'s level: {self.level}")

    def display_color(self):
        print(f"{self.name}'s race: {self.color}")