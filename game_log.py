class GameLog:
    def __init__(self):
        self.history = []
        self.action_stats = {
            'persuadir': {'total': 0, 'success': 0},
            'propor_alianca': {'total': 0, 'success': 0},
            'manipular_rumores': {'total': 0, 'success': 0}
        }
        self.support_history = []

    def log_action(self, action_type, target, success, impact):
        """Registra uma ação com detalhes."""
        self.history.append({
            'timestamp': self.get_round_time(),
            'type': action_type,
            'target': target.name,
            'success': success,
            'impact': f"{impact:+.1f}%",
            'details': f"Ação {'bem-sucedida' if success else 'falhou'} com impacto de {impact:+.1f}%."
        })
        # Atualiza estatísticas
        self.action_stats[action_type]['total'] += 1
        if success:
            self.action_stats[action_type]['success'] += 1

    def log_message(self, message):
        """Registra uma mensagem simples no histórico."""
        self.history.append({
            'timestamp': self.get_round_time(),
            'type': 'message',
            'content': message
        })

    def get_round_time(self):
        """Retorna um timestamp simples baseado na rodada atual."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

    def display_effectiveness_report(self):
        """Exibe relatório de efetividade das ações."""
        print("\n=== Relatório de Efetividade ===")
        for action, stats in self.action_stats.items():
            success_rate = (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"\n{action.title()}:")
            print(f"├── Total de tentativas: {stats['total']}")
            print(f"├── Taxa de sucesso: {success_rate:.1f}%")
            print(f"└── Média de impacto: {self.calculate_average_impact(action):.1f}%")

    def display_support_trend(self, last_n_rounds=5):
        """Exibe tendência de suporte com gráfico ASCII."""
        print("\n=== Tendência de Suporte ===")
        for round_num, support in enumerate(self.support_history[-last_n_rounds:], 1):
            bar_length = int(support / 2)
            print(f"Rodada {round_num}: [{'█' * bar_length}{'·' * (50-bar_length)}] {support}%")

    def display_strategic_alerts(self):
        """Exibe alertas estratégicos baseados nas mudanças recentes."""
        print("\n🔔 Alertas Estratégicos:")
        for faction in self.factions:
            support_change = self.calculate_support_change(faction)
            if support_change > 10:
                print(f"📈 Oportunidade: Suporte crescendo na facção {faction.name}")
            elif support_change < -10:
                print(f"⚠️ Alerta: Queda significativa no suporte da facção {faction.name}")

    def display_round_summary(self):
        """Exibe resumo detalhado da rodada atual."""
        print("\n📊 Resumo da Rodada:")
        print("\nAções realizadas:")
        for action in self.current_round_actions:
            success_icon = "✅" if action['success'] else "❌"
            print(f"{success_icon} {action['type']} → {action['target']}: {action['impact']:+.1f}%")
        
        print("\nMudanças de Suporte:")
        for faction in self.factions:
            change = self.calculate_support_change(faction)
            trend = "↗️" if change > 0 else "↘️" if change < 0 else "→"
            print(f"{trend} {faction.name}: {change:+.1f}%")
