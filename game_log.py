class GameLog:
    def __init__(self):
        self.history = []

    def log_action(self, action: str):
        """Adiciona uma ação ao histórico."""
        self.history.append(action)

    def get_history(self):
        """Retorna o histórico completo."""
        return self.history

    def clear_history(self):
        """Limpa o histórico."""
        self.history = []

    def display_history(self):
        """Exibe o histórico de ações."""
        print("\n=== Histórico de Ações ===")
        for idx, action in enumerate(self.history, start=1):
            print(f"{idx}. {action}")
        print("==========================")
