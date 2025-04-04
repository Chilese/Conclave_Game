import logging
from datetime import datetime
from typing import Dict, List, Any

class GameLogger:
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.action_stats = {
            'persuadir': {'total': 0, 'success': 0},
            'propor_alianca': {'total': 0, 'success': 0},
            'manipular_rumores': {'total': 0, 'success': 0}
        }
        self.support_history: List[Dict[str, float]] = []
        self.stats: Dict[str, List[float]] = {}

        # Configuração do logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('conclave_game')

    def log_action(self, action_type: str, target: str, success: bool, impact: float) -> None:
        """Registra uma ação com detalhes."""
        self.history.append({
            'timestamp': self._get_timestamp(),
            'type': action_type,
            'target': target,
            'success': success,
            'impact': f"{impact:+.1f}%",
            'details': f"Ação {'bem-sucedida' if success else 'falhou'} com impacto de {impact:+.1f}%."
        })
        
        self.action_stats[action_type]['total'] += 1
        if success:
            self.action_stats[action_type]['success'] += 1

    def log_stat(self, stat_name: str, value: float) -> None:
        """Registra uma estatística."""
        if stat_name not in self.stats:
            self.stats[stat_name] = []
        self.stats[stat_name].append(value)

    def log_support_change(self, faction_name: str, candidate_name: str, old_support: float, new_support: float) -> None:
        """Registra mudança no suporte de um candidato."""
        self.support_history.append({
            'timestamp': self._get_timestamp(),
            'faction': faction_name,
            'candidate': candidate_name,
            'old_support': old_support,
            'new_support': new_support,
            'change': new_support - old_support
        })

    def display_action_history(self) -> None:
        """Exibe o histórico de ações formatado."""
        print("\n=== Histórico de Ações ===")
        for action in self.history:
            print(f"[{action['timestamp']}] {action['type']} -> {action['target']}: {action['impact']}")
        print("=" * 30)

    def display_statistics(self) -> None:
        """Exibe estatísticas do jogo."""
        print("\n=== Estatísticas do Jogo ===")
        self._display_action_stats()
        self._display_support_trends()
        print("=" * 30)

    def _display_action_stats(self) -> None:
        """Exibe estatísticas de ações."""
        print("\nEfetividade das Ações:")
        for action, stats in self.action_stats.items():
            success_rate = (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"{action}:")
            print(f"  Total: {stats['total']}")
            print(f"  Taxa de Sucesso: {success_rate:.1f}%")

    def _display_support_trends(self) -> None:
        """Exibe tendências de suporte."""
        if not self.support_history:
            return

        print("\nTendências de Suporte:")
        latest_changes = {}
        for change in self.support_history[-5:]:  # Últimas 5 mudanças
            faction = change['faction']
            if faction not in latest_changes:
                latest_changes[faction] = []
            latest_changes[faction].append(change['change'])

        for faction, changes in latest_changes.items():
            avg_change = sum(changes) / len(changes)
            trend = "↑" if avg_change > 0 else "↓" if avg_change < 0 else "→"
            print(f"{faction}: {trend} ({avg_change:+.1f}%)")

    def _get_timestamp(self) -> str:
        """Retorna timestamp formatado."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def debug(self, message: str) -> None:
        """Registra mensagem de debug."""
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """Registra mensagem informativa."""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Registra mensagem de aviso."""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Registra mensagem de erro."""
        self.logger.error(message)