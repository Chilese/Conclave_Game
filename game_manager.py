from typing import Dict, List
from Cardinal import Cardinal
from Faction import Faction
from Event import Event

class GameManager:
    """Gerencia o estado e as mecânicas principais do jogo."""
    
    def __init__(self):
        self.total_cardinals = 206
        self.npc_cardinals = 205
        self.rounds = 0
        self._action_history: List[str] = []
    
    def log_action(self, action: str) -> None:
        """Registra uma ação no histórico."""
        self._action_history.append(action)
    
    def get_action_history(self) -> List[str]:
        """Retorna o histórico de ações."""
        return self._action_history.copy()
    
    def validate_game_state(self) -> bool:
        """Valida o estado atual do jogo."""
        # Implementar validações
        return True
