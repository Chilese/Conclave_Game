from enum import Enum
from typing import Dict
from dataclasses import dataclass

class EffectType(Enum):
    MODIFICAR_VOTOS = "modificar_votos"
    ALTERAR_REPUTACAO = "alterar_reputacao"
    MODIFICAR_INFLUENCIA = "modificar_influencia"

@dataclass
class Effect:
    type: EffectType
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
            case EffectType.MODIFICAR_VOTOS:
                game_state.player_votes += self.magnitude
            case EffectType.ALTERAR_REPUTACAO:
                if self.target in game_state.reputation:
                    game_state.reputation[self.target] += self.magnitude
            case EffectType.MODIFICAR_INFLUENCIA:
                if self.target in game_state.player_influence:
                    game_state.player_influence[self.target] += self.magnitude

        self.rounds_remaining -= 1
        return True

    def get_description(self) -> str:
        """Retorna descrição legível do efeito"""
        base_desc = ""
        match self.type:
            case EffectType.MODIFICAR_VOTOS:
                base_desc = f"{'Aumenta' if self.magnitude > 0 else 'Diminui'} votos em {abs(self.magnitude)}"
            case EffectType.ALTERAR_REPUTACAO:
                base_desc = f"{'Melhora' if self.magnitude > 0 else 'Piora'} reputação com {self.target} em {abs(self.magnitude)}"
            case EffectType.MODIFICAR_INFLUENCIA:
                base_desc = f"{'Aumenta' if self.magnitude > 0 else 'Diminui'} influência com {self.target} em {abs(self.magnitude)}"
        
        return f"{base_desc} por {self.duration} rodadas"