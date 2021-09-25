class Case:
    def __init__(self, energy, capital, timeline) -> None:
        self.energy = energy
        self.capital = capital
        self.timeline = timeline
    
    def __str__(self) -> str:
        return str(self.energy) + str(self.capital) + str(self.timeline)