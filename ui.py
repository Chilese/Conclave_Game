def get_input(prompt, options, default=None):
    print(prompt)
    if isinstance(options, list):
        for i, option in enumerate(options):
            print(f"{i}. {option}")  # Exibe opções numeradas
        while True:
            choice = input("Escolha (número): ")
            try:
                idx = int(choice)
                if 0 <= idx < len(options):
                    return idx  # Retorna o índice como inteiro
                else:
                    print(f"Por favor, escolha um número entre 0 e {len(options)-1}.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
    return input("Digite: ") or default

def show_menu(prompt, options):
    display_info(prompt)
    for i, option in enumerate(options):
        display_info(f"{i}. {option}")
    return int(input("Escolha (número): "))

def display_info(message):
    print(message)