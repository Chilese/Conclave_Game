def get_input(prompt, min_val=None, max_val=None, options=None, default=None):
    """Função unificada de input que aceita tanto opções numéricas quanto lista de escolhas"""
    if options is not None:
        display_info(prompt)
        display_options(options)
        while True:
            choice = input("Escolha (número): ")
            if choice.lower() in ['q', 'quit', 'sair']:
                return -1
            try:
                idx = int(choice)
                if 0 <= idx < len(options):
                    return idx
                display_info(f"Por favor, escolha um número entre 0 e {len(options)-1}.")
            except ValueError:
                display_info("Entrada inválida. Digite um número.")
    else:
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

def display_info(message, separator=False):
    """Exibe informação com separador opcional."""
    if separator:
        print("\n" + "="*50)
    print(message)
    if separator:
        print("="*50)

def display_options(options, show_attributes=False):
    """Exibe opções numeradas com atributos opcionais."""
    print("\nOpções disponíveis:")
    for i, option in enumerate(options):
        if isinstance(option, str):
            print(f"  [{i}] {option}")
        else:  # Se for um cardeal
            ideology = getattr(option, 'ideology', 'Desconhecido')
            print(f"  [{i}] {option.name} ({ideology})")
    print()

def display_feedback(action: str, candidate_name: str, faction_name: str, previous_support: float, new_support: float) -> None:
    """Exibe feedback sobre o impacto de uma ação no suporte de um candidato."""
    change = new_support - previous_support
    result_text = "Sucesso!" if change > 0 else "Falha" if change < 0 else "Neutro"
    message = (
        f"\nResultado da Ação\n"
        f"Tipo: {action}\n"
        f"Candidato: {candidate_name}\n"
        f"Facção: {faction_name}\n"
        f"\nResultado: {result_text}\n"
        f"\nMudança de Suporte:\n"
        f"  Anterior: {previous_support:.1f}%\n"
        f"  Atual:    {new_support:.1f}%\n"
        f"  Variação: {change:+.1f}%\n"
    )
    print(message)

def display_voting_results(candidate_votes, total_voters):
    """Exibe resultados da votação com formatação melhorada."""
    required_majority = int(total_voters * 2 / 3) + 1
    display_info("\n=== Resultados da Votação ===", separator=True)
    
    sorted_results = sorted(candidate_votes.items(), key=lambda x: x[1], reverse=True)
    leader = sorted_results[0]
    leader_percentage = (leader[1] / total_voters) * 100
    
    print(f"\n📊 Total de votos: {total_voters}")
    print(f"🎯 Votos necessários para vitória: {required_majority} (2/3)")
    print(f"\n👑 Líder atual: {leader[0].name}")
    print(f"   Votos: {leader[1]} ({leader_percentage:.1f}%)")
    
    print("\nResultados completos:")
    print("-" * 50)
    for candidate, votes in sorted_results:
        percentage = (votes / total_voters) * 100
        bar_length = int(percentage / 2)
        bar = "█" * bar_length + "░" * (50 - bar_length)
        print(f"{candidate.name:15} [{bar:50}] {votes:3d} ({percentage:5.1f}%)")
    
    print("-" * 50)