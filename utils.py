def get_input(prompt, min_val, max_val, default=None):
    while True:
        try:
            value = input(f"{prompt} ({min_val}-{max_val}): ")
            if value == "" and default is not None:
                return default
            value = int(value)
            if min_val <= value <= max_val:
                return value
            print(f"Digite um valor entre {min_val} e {max_val}.")
        except ValueError:
            print("Digite um número válido.")

def normalize_support(support_dict):
    """Normaliza os valores de suporte para que somem 100%."""
    total = sum(support_dict.values())
    if total > 0:
        for key in support_dict:
            support_dict[key] = (support_dict[key] / total) * 100

def show_menu(prompt, options):
    display_info(prompt)
    display_options(options)  # Reutiliza a função auxiliar para exibir opções    print(f"Suporte normalizado: {support_dict}")  # Log para depuração
    while True:
        try:
            return int(input("Escolha (número): "))
        except ValueError:
            display_info("Entrada inválida. Digite um número.")

def display_info(message):
    print(message)
def display_options(options):
    """Exibe uma lista de opções numeradas."""
    for i, option in enumerate(options):
        display_info(f"{i}. {option}")

# Função adicionada para resolver o erro de importaçãoas."""
def display_feedback(action: str, candidate_name: str, faction_name: str, previous_support: float, new_support: float) -> None:
    """
    Exibe feedback sobre o impacto de uma ação no suporte de um candidato.
    """
    change = new_support - previous_support
    message = (
        f"{action} realizada com sucesso!\n"
        f"Suporte ao {candidate_name} na facção {faction_name}:\n"
        f"  Antes: {previous_support:.2f}%\n"
        f"  Depois: {new_support:.2f}%\n"
        f"  Mudança: {change:.2f}%"
    )
    print(message)