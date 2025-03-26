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
    display_info("\nResultado da Ação", separator=True)
    print(f"Tipo: {action_type}")
    print(f"Alvo: {target}")
    
    change = after - before
    result_text = "Sucesso!" if change > 0 else "Falha" if change < 0 else "Neutro"
    print(f"\nResultado: {result_text}")
    
    print("\nMudança de Suporte:")
    print(f"  Anterior: {before:.1f}%")
    print(f"  Atual:    {after:.1f}%")
    print(f"  Variação: {change:+.1f}%")
    
    if change > 0:
        print("\n✅ Ação bem-sucedida!")
    elif change < 0:
        print("\n⚠️ A ação teve efeito negativo!")
    else:
        print("\nℹ️ A ação não teve efeito significativo.")