from typing import Dict

def normalize_support(support_dict: Dict[str, float]) -> None:
    """Normaliza os valores de suporte para que somem 100%."""
    total_support = sum(support_dict.values())
    if total_support > 0:
        for candidate in support_dict:
            support_dict[candidate] = (support_dict[candidate] / total_support) * 100

def display_feedback(action: str, candidate_name: str, faction_name: str, previous_support: float, new_support: float) -> None:
    """Exibe feedback detalhado sobre mudanças de suporte."""
    message = (
        f"{action} bem-sucedida! Suporte ao {candidate_name} na facção {faction_name}:\n"
        f"  Antes: {previous_support:.2f}%\n"
        f"  Depois: {new_support:.2f}%\n"
        f"  Mudança: {new_support - previous_support:.2f}%"
    )
    print(message)  # Garante que o feedback seja exibido no terminal

def display_info(message: str) -> None:
    """Exibe uma mensagem informativa para o jogador."""
    print(f"[INFO] {message}")
