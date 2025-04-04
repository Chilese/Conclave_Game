def get_input(prompt, options, default=None):
    display_info(prompt)
    if isinstance(options, list):
        display_options(options)  # Reutiliza a função auxiliar para exibir opções
        while True:
            choice = input("Escolha (número): ")
            try:
                idx = int(choice)
                if 0 <= idx < len(options):
                    return idx  # Retorna o índice como inteiro
                else:
                    display_info(f"Por favor, escolha um número entre 0 e {len(options)-1}.")
            except ValueError:
                display_info("Entrada inválida. Digite um número.")
    return input("Digite: ") or default

def show_menu(prompt, options):
    """Exibe menu com formatação melhorada."""
    display_info(prompt, separator=True)
    display_options(options)
    while True:
        try:
            choice = input("Digite o número da sua escolha: ")
            if choice.lower() in ['q', 'quit', 'sair']:
                return -1
            idx = int(choice)
            if 0 <= idx < len(options):
                return idx
            print(f"\nEscolha inválida. Digite um número entre 0 e {len(options)-1}.")
        except ValueError:
            print("\nEntrada inválida. Digite um número ou 'q' para sair.")

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

def display_action_feedback(action_type, target, result, before, after):
    """Exibe feedback de ação com formatação melhorada."""
    change = after - before
    result_text = "Sucesso!" if change > 0 else "Falha" if change < 0 else "Neutro"
    feedback = (
        f"\nResultado da Ação\n"
        f"Tipo: {action_type}\n"
        f"Alvo: {target}\n"
        f"\nResultado: {result_text}\n"
        f"\nMudança de Suporte:\n"
        f"  Anterior: {before:.1f}%\n"
        f"  Atual:    {after:.1f}%\n"
        f"  Variação: {change:+.1f}%\n"
    )
    print(feedback)
    return feedback

def display_voting_results(candidate_votes, total_voters):
    """Exibe resultados da votação com formatação melhorada."""
    required_majority = int(total_voters * 2 / 3) + 1
    display_info("\n=== Resultados da Votação ===", separator=True)
    
    # Ordenar candidatos por número de votos
    sorted_results = sorted(candidate_votes.items(), key=lambda x: x[1], reverse=True)
    
    # Encontrar o líder
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
        bar_length = int(percentage / 2)  # Ajustado para melhor visualização
        bar = "█" * bar_length + "░" * (25 - bar_length)  # Reduzido tamanho da barra
        print(f"{candidate.name:15} [{bar:25}] {votes:3d} ({percentage:5.1f}%)")
    
    print("-" * 50)