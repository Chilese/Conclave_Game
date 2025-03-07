def get_input(prompt, options, default=None):
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    choice = int(input("Digite o número correspondente: "))
    if 1 <= choice <= len(options):
        return options[choice - 1]
    print(f"Escolha inválida. Usando padrão: {default}")
    return default

def show_menu(prompt, items, exit_option=True):
    print(prompt)
    for i, item in enumerate(items, 1):
        print(f"{i}. {item}")
    if exit_option:
        print("0. Sair")
    choice = int(input("Digite o número correspondente: "))
    return choice

def display_info(message):
    print(message)