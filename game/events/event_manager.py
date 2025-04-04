class DynamicEventManager:
    def __init__(self):
        self.events = []
        self.active_events = []
        self.event_history = []
    
    def add_event(self, event, priority=0):
        """Adiciona um evento com prioridade"""
        self.events.append((priority, event))
        self.events.sort(reverse=True)  # Ordena por prioridade
    
    def update(self, game_state):
        """Atualiza e processa eventos ativos"""
        processed_events = []
        for priority, event in self.events:
            if event.check_conditions(game_state):
                event.trigger_event(game_state)
                self.event_history.append(event)
                processed_events.append((priority, event))
        # Remove eventos processados
        self.events = [e for e in self.events if e not in processed_events]
