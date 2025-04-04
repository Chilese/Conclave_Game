class DynamicEvent:
    def __init__(self, event_type, trigger, conditions, effects):
        self.event_type = event_type
        self.trigger = trigger
        self.conditions = conditions
        self.effects = effects
        self.is_active = False
        self.chain_events = []
    
    def check_conditions(self, game_state):
        """Verifica se as condições para o evento estão satisfeitas"""
        return all(condition(game_state) for condition in self.conditions)
    
    def trigger_event(self, game_state):
        """Ativa o evento e seus efeitos"""
        if self.check_conditions(game_state):
            self.is_active = True
            for effect in self.effects:
                effect(game_state)
            self.trigger_chain_events(game_state)
    
    def add_chain_event(self, event):
        """Adiciona um evento à cadeia"""
        self.chain_events.append(event)
    
    def trigger_chain_events(self, game_state):
        """Ativa eventos encadeados"""
        for event in self.chain_events:
            event.trigger_event(game_state)
