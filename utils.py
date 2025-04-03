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

def normalize_support(support_dict, min_value=2.0):
    """Normaliza os valores de suporte garantindo impacto mínimo das ações."""
    log_debug("\n=== INÍCIO DA NORMALIZAÇÃO ===")
    log_debug("Valores iniciais:")
    for candidate, support in support_dict.items():
        log_debug(f"- {candidate.name}: {support:.2f}%")
    
    total = sum(support_dict.values())
    log_debug(f"Total inicial: {total:.2f}%")
    
    if total <= 0:
        log_debug("Total zero ou negativo - normalização abortada")
        return
        
    if total > 100:
        excess = total - 100
        # Distribuir o excesso proporcionalmente
        for candidate in support_dict:
            reduction = (support_dict[candidate] / total) * excess
            support_dict[candidate] = max(min_value, support_dict[candidate] - reduction)
    
    # Garantir que a soma seja 100%
    total = sum(support_dict.values())
    if total != 100:
        factor = 100 / total
        for candidate in support_dict:
            support_dict[candidate] = max(min_value, support_dict[candidate] * factor)
    
    log_debug("\nValores finais após normalização:")
    for candidate, support in support_dict.items():
        log_debug(f"- {candidate.name}: {support:.2f}%")
    log_debug(f"Total final: {sum(support_dict.values()):.2f}%")
    log_debug("=== FIM DA NORMALIZAÇÃO ===\n")

def log_debug(message):
    DEBUG_MODE = True  # Alterar para False em produção
    if DEBUG_MODE:
        print(f"DEBUG: {message}")

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