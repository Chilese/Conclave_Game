class GameStatistics:
    def __init__(self):
        self.stats = {}

    def record_stat(self, stat_name: str, value: float):
        """Registra uma estatística."""
        if stat_name not in self.stats:
            self.stats[stat_name] = []
        self.stats[stat_name].append(value)

    def get_statistics(self):
        """Retorna todas as estatísticas registradas."""
        return self.stats

    def display_statistics(self):
        """Exibe as estatísticas de forma organizada."""
        print("\n=== Estatísticas do Jogo ===")
        for stat_name, values in self.stats.items():
            print(f"{stat_name}: {values}")
        print("=============================")
