class Event:
    def __init__(self, name, effect, duration, event_type):
        self.name = name
        self.effect = effect  # Função lambda ou método
        self.duration = duration
        self.type = event_type  # "positive", "negative", "neutral"