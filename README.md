# Conclave Game 🎮

Um jogo de estratégia baseado em texto que simula a dinâmica de um conclave papal, onde os jogadores assumem o papel de um cardeal tentando influenciar a eleição do próximo Papa através de negociações, alianças e manobras políticas.

## 📋 Descrição

Conclave Game é um simulador político onde você assume o papel de um cardeal em um conclave papal. O objetivo é usar sua influência, carisma, erudição e discrição para apoiar seu candidato favorito e garantir sua eleição como Papa.

## 🎯 Características Principais

- Sistema de atributos para cardeais (Influência, Carisma, Erudição, Discrição)
- Mecânica de facções com diferentes ideologias (Conservadores, Moderados, Progressistas)
- Sistema dinâmico de votação
- Eventos aleatórios que afetam o conclave
- Diferentes estratégias de interação (Persuasão, Alianças, Manipulação)
- Sistema de feedback detalhado sobre o impacto das ações

## 🚀 Começando

### Pré-requisitos

- Python 3.7 ou superior

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/conclave-game.git
cd conclave-game
```

### Executando o jogo

```bash
python Main.py
```

## 🎮 Como Jogar

1. Configure seu cardeal:
   - Escolha um nome
   - Defina sua faixa etária
   - Selecione sua região
   - Distribua pontos entre seus atributos

2. Escolha seu candidato favorito

3. Durante cada rodada, você pode:
   - Persuadir outros cardeais
   - Propor alianças
   - Manipular rumores
   - Participar das votações

4. O jogo continua até que um candidato alcance 2/3 dos votos necessários

## 🏗️ Estrutura do Projeto

```
conclave-game/
│
├── Cardinal.py          # Classe base para cardeais
├── Candidate.py         # Classe para candidatos
├── Event.py             # Sistema de eventos
├── Faction.py           # Sistema de facções
├── Game.py              # Lógica principal do jogo
├── Interactions.py      # Sistema de interações
├── Main.py              # Ponto de entrada do jogo
├── rules.py             # Regras do jogo
├── utils.py             # Funções utilitárias
└── ui.py                # Interface do usuário
```

## 🛠️ Tecnologias Utilizadas

- Python 3
- Programação Orientada a Objetos
- Design Patterns (Observer, Strategy)

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## ✍️ Autores

* **Seu Nome** - *Trabalho Inicial* - [SeuUsuario](https://github.com/SeuUsuario)

## 📝 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes

## 🎯 Status do Projeto

⚙️ Em desenvolvimento

## 🔮 Funcionalidades Futuras

- [ ] Interface gráfica
- [ ] Modo multiplayer
- [ ] Sistema de conquistas
- [ ] Eventos históricos
- [ ] Perfis de cardeais históricos
