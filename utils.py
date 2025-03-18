def normalize_support(support_dict):
    """Normaliza os valores de suporte para que somem 100%."""
    total_support = sum(support_dict.values())
    if total_support > 0:
        for candidate in support_dict:
            support_dict[candidate] = (support_dict[candidate] / total_support) * 100

def display_feedback(action, candidate_name, faction_name, previous_support, new_support):
    """Exibe feedback detalhado sobre mudanças de suporte."""
    message = (
        f"{action} bem-sucedida! Suporte ao {candidate_name} na facção {faction_name}:\n"
        f"  Antes: {previous_support:.2f}%\n"
        f"  Depois: {new_support:.2f}%\n"
        f"  Mudança: {new_support - previous_support:.2f}%"
    )
    print(message)  # Garante que o feedback seja exibido no terminal

def display_info(message: str):
    """
    Exibe uma mensagem informativa para o jogador.
    :param message: Mensagem a ser exibida
    """
    print(f"[INFO] {message}")
