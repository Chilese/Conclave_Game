from enum import Enum
from typing import Dict, List, Callable, Optional
from dataclasses import dataclass

class ConditionType(Enum):
    RODADA = "rodada"
    VOTOS = "votos"
    INFLUENCIA = "influencia"
    ALIANCA = "alianca"
    REPUTACAO = "reputacao"

class EventType(Enum):
    FACTION = "faction"
    REACTIVE = "reactive"
    CHAIN = "chain"
    CRISIS = "crisis"
    OPPORTUNITY = "opportunity"
    MODIFICAR_VOTOS = "modificar_votos"
    ALTERAR_REPUTACAO = "alterar_reputacao"
    MODIFICAR_INFLUENCIA = "modificar_influencia"

class EventTrigger(Enum):
    PLAYER_ACTION = "player_action"
    FACTION_STATUS = "faction_status"
    ROUND_START = "round_start"
    ALLIANCE_FORMED = "alliance_formed"

@dataclass
class GameState:
    current_round: int
    player_votes: int
    player_influence: dict
    alliances: list
    reputation: dict

@dataclass
class EventEffect:
    type: EventType
    magnitude: int
    duration: int
    target: str = None
    rounds_remaining: int = None

    def __post_init__(self):
        self.rounds_remaining = self.duration

    def apply(self, game_state) -> bool:
        """Aplica o efeito ao estado do jogo"""
        if self.rounds_remaining <= 0:
            return False

        match self.type:
            case EventType.MODIFICAR_VOTOS:
                game_state.player_votes += self.magnitude
            case EventType.ALTERAR_REPUTACAO:
                if self.target in game_state.reputation:
                    game_state.reputation[self.target] += self.magnitude
            case EventType.MODIFICAR_INFLUENCIA:
                if self.target in game_state.player_influence:
                    game_state.player_influence[self.target] += self.magnitude

        self.rounds_remaining -= 1
        return True

    def get_description(self) -> str:
        """Retorna descrição legível do efeito"""
        base_desc = ""
        match self.type:
            case EventType.MODIFICAR_VOTOS:
                base_desc = f"{'Aumenta' if self.magnitude > 0 else 'Diminui'} votos em {abs(self.magnitude)}"
            case EventType.ALTERAR_REPUTACAO:
                base_desc = f"{'Melhora' if self.magnitude > 0 else 'Piora'} reputação com {self.target} em {abs(self.magnitude)}"
            case EventType.MODIFICAR_INFLUENCIA:
                base_desc = f"{'Aumenta' if self.magnitude > 0 else 'Diminui'} influência com {self.target} em {abs(self.magnitude)}"
        
        return f"{base_desc} por {self.duration} rodadas"

class EventCondition:
    def __init__(self, condition_type: ConditionType, parameters: Dict):
        self.type = condition_type
        self.parameters = parameters
    
    def check(self, game_state: GameState) -> bool:
        """Verifica se a condição é atendida"""
        match self.type:
            case ConditionType.RODADA:
                return game_state.current_round == self.parameters["rodada"]
            case ConditionType.VOTOS:
                return game_state.player_votes >= self.parameters["min_votos"]
            case ConditionType.INFLUENCIA:
                faccao = self.parameters["faccao"]
                return game_state.player_influence.get(faccao, 0) >= self.parameters["valor"]
            case _:
                return False

    def get_description(self) -> str:
        """Retorna descrição legível da condição"""
        match self.type:
            case ConditionType.RODADA:
                return f"Acontece na rodada {self.parameters['rodada']}"
            case ConditionType.VOTOS:
                return f"Requer {self.parameters['min_votos']} votos"
            case ConditionType.INFLUENCIA:
                return f"Requer {self.parameters['valor']} de influência com {self.parameters['faccao']}"
            case _:
                return "Condição desconhecida"

class EventManager:
    def __init__(self):
        self.events = []
        self.active_events = []
        self.event_history = []
        self._event_handlers: Dict[str, List[Callable]] = {}
    
    def add_event(self, event, priority=0):
        """Adiciona um evento com prioridade"""
        self.events.append((priority, event))
        self.events.sort(reverse=True)
    
    def subscribe(self, event_name: str, callback: Callable) -> None:
        """Registra um callback para um tipo de evento"""
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = []
        self._event_handlers[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable) -> None:
        """Remove um callback registrado"""
        if event_name in self._event_handlers:
            self._event_handlers[event_name].remove(callback)

    def trigger(self, event_name: str, **kwargs) -> None:
        """Dispara um evento para todos os handlers registrados"""
        if event_name in self._event_handlers:
            for callback in self._event_handlers[event_name]:
                callback(**kwargs)
    
    def update(self, game_state):
        """Atualiza e processa eventos ativos"""
        processed_events = []
        for priority, event in self.events:
            if event.check_conditions(game_state):
                event.trigger_event(game_state)
                self.event_history.append(event)
                processed_events.append((priority, event))
        
        self.events = [e for e in self.events if e not in processed_events]