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
    display_info(prompt)
    display_options(options)  # Reutiliza a função auxiliar para exibir opções
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