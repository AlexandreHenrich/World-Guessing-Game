import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import requests
import random
import math
from datetime import datetime


class BancoDados:
    def __init__(self):
        self.conexao = sqlite3.connect("ranking.db")
        self.cursor = self.conexao.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ranking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jogador TEXT NOT NULL,
                pontuacao INTEGER NOT NULL,
                data_hora TEXT NOT NULL
            )
        """)
        self.conexao.commit()

    def salvar_recorde(self, jogador, pontuacao):
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
            INSERT INTO ranking (jogador, pontuacao, data_hora)
            VALUES (?, ?, ?)
        """, (jogador, pontuacao, data_hora))
        self.conexao.commit()

    def listar_top5(self):
        self.cursor.execute("""
            SELECT jogador, pontuacao, data_hora
            FROM ranking
            ORDER BY pontuacao DESC
            LIMIT 5
        """)
        return self.cursor.fetchall()



class ServicoAPI:
    def __init__(self):
        self.url = "https://restcountries.com/v3.1/all?fields=name,capital,population,flags,region"
        self.paises = []
        self.carregar_paises()

    def carregar_paises(self):
        resposta = requests.get(self.url)
        if resposta.status_code == 200:
            self.paises = resposta.json()
        else:
            print("Erro ao acessar a API")

    def pais_aleatorio(self):
        return random.choice(self.paises)



class JogoApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("World Guessing Game")
        self.geometry("600x600")

        self.jogador = ""


        self.frame_inicio = tk.Frame(self)
        self.frame_inicio.pack(expand=True)

        lbl_nome = tk.Label(self.frame_inicio, text="Digite seu nome:", font=("Arial", 12))
        lbl_nome.pack(pady=10)

        self.entry_nome = tk.Entry(self.frame_inicio, font=("Arial", 12))
        self.entry_nome.pack(pady=5)

        btn_iniciar = tk.Button(
            self.frame_inicio,
            text="Iniciar Jogo",
            command=self.iniciar_jogo
        )
        btn_iniciar.pack(pady=10)

        
        

        self.frame_jogo = tk.Frame(self)

        self.api = ServicoAPI()
        self.banco = BancoDados()

        self.pais_atual = None
        self.inicio_rodada = None

        self.lbl_titulo = tk.Label(
            self.frame_jogo,
            text="🌍 World Guessing Game",
            font=("Arial", 18, "bold")
        )
        self.lbl_titulo.pack(pady=10)


        self.lbl_dica = tk.Label(self.frame_jogo, text="", font=("Arial", 12))
        self.lbl_dica.pack(pady=10)

        self.entry_palpite = tk.Entry(self.frame_jogo, font=("Arial", 12))
        self.entry_palpite.pack(pady=5)

        self.btn_chutar = tk.Button(self.frame_jogo, text="Chutar", command=self.verificar_palpite)
        self.btn_chutar.pack(pady=10)

        
        self.lbl_ranking = tk.Label(self, text="🏆 Top 5 Jogadores", font=("Arial", 12, "bold"))
        self.lbl_ranking.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("jogador", "pontuacao", "data"), show="headings")
        self.tree.heading("jogador", text="Jogador")
        self.tree.heading("pontuacao", text="Pontuação")
        self.tree.heading("data", text="Data/Hora")

        self.tree.column("jogador", width=150)
        self.tree.column("pontuacao", width=100, anchor="center")
        self.tree.column("data", width=200)

        self.tree.pack(pady=5)

        self.atualizar_ranking()
        self.nova_rodada()



    def atualizar_ranking(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        registros = self.banco.listar_top5()
        for jogador, pontuacao, data in registros:
            self.tree.insert("", tk.END, values=(jogador, pontuacao, data))



    def nova_rodada(self):
        self.pais_atual = self.api.pais_aleatorio()

        capital = self.pais_atual.get("capital", ["Sem capital"])[0]
        continente = self.pais_atual.get("region", "Desconhecido")

        self.lbl_dica.config(
            text=f"Dica:\nCapital: {capital}\nContinente: {continente}"
        )

        self.entry_palpite.delete(0, tk.END)
        self.inicio_rodada = datetime.now()

    def verificar_palpite(self):
        palpite = self.entry_palpite.get().strip()
        resposta = self.pais_atual["name"]["common"]

        fim_rodada = datetime.now()
        tempo_gasto = (fim_rodada - self.inicio_rodada).total_seconds()

        if palpite.lower() == resposta.lower():
            pontos = calcular_pontuacao(
                tempo_gasto,
                self.pais_atual["population"]
            )

            self.banco.salvar_recorde(self.jogador, pontos)
            self.atualizar_ranking()


            messagebox.showinfo(
                "Acertou!",
                f"Você acertou!\nPontuação: {pontos}"
            )

            self.nova_rodada()
        else:
            messagebox.showerror("Errou", "País incorreto. Novo país sorteado!")
            self.nova_rodada()


    def iniciar_jogo(self):
        nome = self.entry_nome.get().strip()

        if nome == "":
            messagebox.showwarning("Atenção", "Digite seu nome!")
            return

        self.jogador = nome

        self.frame_inicio.pack_forget()
        self.frame_jogo.pack(expand=True)

        self.nova_rodada()




def calcular_pontuacao(tempo_gasto, populacao):
    if tempo_gasto <= 5:
        pontos_base = 1000
    elif tempo_gasto <= 10:
        pontos_base = 700
    elif tempo_gasto <= 20:
        pontos_base = 400
    else:
        pontos_base = 200

    bonus = math.floor(100 / math.log10(populacao))
    return pontos_base + bonus



if __name__ == "__main__":
    app = JogoApp()
    app.mainloop()

    