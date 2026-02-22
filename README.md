# 🌍 World Guessing Game (Ranking Edition)

Um jogo de conhecimentos geográficos interativo desenvolvido em Python. O desafio é adivinhar o país sorteado com base em sua capital e continente, consumindo dados em tempo real da API pública *REST Countries*. 

O jogo se destaca por um sistema de pontuação inteligente — que calcula os pontos com base no tempo de resposta e na dificuldade (população do país) — e um placar Top 5 persistente usando banco de dados SQLite.

## 🎮 Como Funciona
O jogador é desafiado a descobrir o nome de um país sorteado aleatoriamente, tendo apenas duas dicas: a **Capital** e o **Continente**. 
A versão "Ranking Edition" possui uma lógica inteligente de pontuação: quanto mais rápido o jogador responder e menor for a população do país sorteado (maior a dificuldade), mais pontos ele ganha!

## ✨ Funcionalidades
- **Consumo de API:** Dados dos países consumidos em tempo real (API *REST Countries*).
- **Cálculo de Pontuação Dinâmico:** Algoritmo matemático que considera o tempo de resposta e a população do país.
- **Sistema de Ranking:** Tabela Top 5 (Leaderboard) que salva os recordes localmente em um Banco de Dados.
- **Interface Gráfica:** Janelas e alertas interativos usando Tkinter para uma melhor experiência do usuário.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3
- **Interface Gráfica (GUI):** Tkinter
- **Banco de Dados:** SQLite3
- **Integração:** Requests (Consumo de API REST)
