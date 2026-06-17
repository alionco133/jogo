import json
import os
import random
import tkinter as tk

ARQUIVO_RANKING = "ranking_copa.json"

# ---------- CORES DO TEMA (inspiradas na Copa do Mundo) ----------
COR_FUNDO = "#0B3D2E" # verde escuro
COR_FUNDO_CARD = "#0E4A37" # verde um pouco mais claro
COR_DESTAQUE = "#FFD700" # dourado (trofeu)
COR_TEXTO = "#FFFFFF"
COR_BOTAO = "#344BBB" # azul
COR_BOTAO_HOVER = "#0044CC"
COR_CERTO = "#1EC362"
COR_ERRADO = "#FDF5F4"

FONTE_TITULO = ("Helvetica", 22, "bold")
FONTE_SUBTITULO = ("Helvetica", 13)
FONTE_PERGUNTA = ("Helvetica", 16, "bold")
FONTE_BOTAO = ("Helvetica", 12, "bold")
FONTE_RANKING = ("Helvetica", 13)

PERGUNTAS = [
    {
        "pergunta": "Quantas vezes o Brasil foi campeao da Copa do Mundo?",
        "opcoes": ["3", "4", "5", "6"],
        "resposta": 2,
    },
    {
        "pergunta": "Qual selecao venceu a Copa do Mundo de 2022, no Catar?",
        "opcoes": ["França", "Argentina", "Brasil", "Croácia"],
        "resposta": 1,
    },
    {
        "pergunta": "Qual pais sediou a primeira Copa do Mundo, em 1930?",
        "opcoes": ["Brasil", "Itália", "Uruguai", "Inglaterra"],
        "resposta": 2,
    },
    {
        "pergunta": "Quantos jogadores cada time coloca em campo (sem contar reservas)?",
        "opcoes": ["9", "10", "11", "12"],
        "resposta": 2,
    },
    {
        "pergunta": "Qual jogador e conhecido como o 'Rei do Futebol'?",
        "opcoes": ["Pelé", "Maradona", "Ronaldinho", "Zidane"],
        "resposta": 0,
    },
    {
        "pergunta": "Em que pais foi realizada a Copa do Mundo de 2014?",
        "opcoes": ["Brasil", "Rússia", "Alemanha", "África do Sul"],
        "resposta": 0,
    },
    {
        "pergunta": "Qual selecao tem o maior numero de titulos da Copa do Mundo?",
        "opcoes": ["Alemanha", "Itália", "Argentina", "Brasil"],
        "resposta": 3,
    },
    {
        "pergunta": "Quantos paises sediarao a Copa do Mundo de 2026?",
        "opcoes": ["1", "2", "3", "4"],
        "resposta": 2,
    },
    {
        "pergunta": "Quem e o maior artilheiro da historia das Copas do Mundo?",
        "opcoes": ["Pelé", "Miroslav Klose", "Ronaldo Fenômeno", "Messi"],
        "resposta": 1,
    },
    {
        "pergunta": "Qual selecao foi vice-campea da Copa do Mundo de 2022?",
        "opcoes": ["Croácia", "Marrocos", "França", "Inglaterra"],
        "resposta": 2,
    },
]


def carregar_ranking():
    if os.path.exists(ARQUIVO_RANKING):
        with open(ARQUIVO_RANKING, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def salvar_ranking(ranking):
    with open(ARQUIVO_RANKING, "w", encoding="utf-8") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=2)


class QuizCopaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz da Copa do Mundo")
        self.root.geometry("640x520")
        self.root.configure(bg=COR_FUNDO)
        self.root.resizable(False, False)

        self.ranking = carregar_ranking()
        self.perguntas = []
        self.indice_atual = 0
        self.pontos = 0
        self.nome = ""

        self.tela_nome()

    # ---------- utilitarios ----------
    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def titulo(self, texto):
        tk.Label(
            self.root, text=texto, font=FONTE_TITULO,
            bg=COR_FUNDO, fg=COR_DESTAQUE, pady=20
        ).pack()

    def botao(self, parent, texto, comando):
        return tk.Button(
            parent, text=texto, font=FONTE_BOTAO,
            bg=COR_BOTAO, fg=COR_TEXTO, activebackground=COR_BOTAO_HOVER,
            relief="flat", padx=14, pady=10, cursor="hand2",
            command=comando
        )

    # ---------- tela 1: nome ----------
    def tela_nome(self):
        self.limpar_tela()
        self.titulo("🏆 QUIZ DA COPA DO MUNDO 🏆")

        tk.Label(
            self.root, text="Digite seu nome para comecar:",
            font=FONTE_SUBTITULO, bg=COR_FUNDO, fg=COR_TEXTO
        ).pack(pady=10)

        self.entry_nome = tk.Entry(self.root, font=("Helvetica", 14), justify="center")
        self.entry_nome.pack(pady=5, ipady=5, ipadx=10)
        self.entry_nome.focus()
        self.entry_nome.bind("<Return>", lambda e: self.iniciar_jogo())

        self.label_erro = tk.Label(
            self.root, text="", font=FONTE_SUBTITULO, bg=COR_FUNDO, fg=COR_ERRADO
        )
        self.label_erro.pack(pady=5)

        self.botao(self.root, "COMEÇAR ⚽", self.iniciar_jogo).pack(pady=20)

        if self.ranking:
            self.botao(self.root, "Ver Ranking", self.tela_ranking).pack()

    def iniciar_jogo(self):
        nome = self.entry_nome.get().strip()
        if not nome:
            self.label_erro.config(text="Por favor, digite um nome.")
            return
        self.nome = nome
        self.perguntas = random.sample(PERGUNTAS, len(PERGUNTAS))
        self.indice_atual = 0
        self.pontos = 0
        self.tela_pergunta()

    # ---------- tela 2: pergunta ----------
    def tela_pergunta(self):
        self.limpar_tela()

        if self.indice_atual >= len(self.perguntas):
            self.tela_resultado()
            return

        item = self.perguntas[self.indice_atual]

        tk.Label(
            self.root,
            text=f"Pergunta {self.indice_atual + 1} de {len(self.perguntas)} | Jogador: {self.nome}",
            font=FONTE_SUBTITULO, bg=COR_FUNDO, fg=COR_DESTAQUE
        ).pack(pady=(20, 10))

        card = tk.Frame(self.root, bg=COR_FUNDO_CARD, padx=20, pady=20)
        card.pack(padx=30, pady=10, fill="both")

        tk.Label(
            card, text=item["pergunta"], font=FONTE_PERGUNTA,
            bg=COR_FUNDO_CARD, fg=COR_TEXTO, wraplength=520, justify="center"
        ).pack(pady=(0, 20))

        letras = ["A", "B", "C", "D"]
        for i, opcao in enumerate(item["opcoes"]):
            texto_botao = f"{letras[i]}) {opcao}"
            self.botao(card, texto_botao, lambda i=i: self.responder(i)).pack(
                fill="x", pady=6
            )

        self.label_feedback = tk.Label(
            self.root, text="", font=FONTE_SUBTITULO, bg=COR_FUNDO, fg=COR_TEXTO
        )
        self.label_feedback.pack(pady=15)

    def responder(self, escolha):
        item = self.perguntas[self.indice_atual]
        correta = item["resposta"]

        # desabilita os botoes para evitar clique duplo
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for botao in widget.winfo_children():
                    if isinstance(botao, tk.Button):
                        botao.config(state="disabled")

        if escolha == correta:
            self.pontos += 10
            self.label_feedback.config(text="✅ Correto!", fg=COR_CERTO)
        else:
            texto_certo = item["opcoes"][correta]
            self.label_feedback.config(
                text=f"❌ Errado! Resposta certa: {texto_certo}", fg=COR_ERRADO
            )

        self.indice_atual += 1
        self.root.after(1300, self.tela_pergunta)

    # ---------- tela 3: resultado ----------
    def tela_resultado(self):
        self.limpar_tela()
        self.titulo("FIM DE JOGO ⚽")

        tk.Label(
            self.root, text=f"{self.nome}, voce marcou:",
            font=FONTE_SUBTITULO, bg=COR_FUNDO, fg=COR_TEXTO
        ).pack(pady=5)

        tk.Label(
            self.root, text=f"{self.pontos} pontos",
            font=("Helvetica", 30, "bold"), bg=COR_FUNDO, fg=COR_DESTAQUE
        ).pack(pady=10)

        self.ranking.append({"nome": self.nome, "pontos": self.pontos})
        salvar_ranking(self.ranking)

        self.botao(self.root, "Ver Ranking 🏆", self.tela_ranking).pack(pady=10)
        self.botao(self.root, "Jogar de novo", self.tela_nome).pack(pady=5)
        self.botao(self.root, "Sair", self.root.destroy).pack(pady=5)

    # ---------- tela 4: ranking ----------
    def tela_ranking(self):
        self.limpar_tela()
        self.titulo("🏆 RANKING DA COPA 🏆")

        card = tk.Frame(self.root, bg=COR_FUNDO_CARD, padx=20, pady=20)
        card.pack(padx=40, pady=10, fill="both")

        ordenado = sorted(self.ranking, key=lambda x: x["pontos"], reverse=True)
        if not ordenado:
            tk.Label(
                card, text="Ainda não há jogadores no ranking.",
                font=FONTE_RANKING, bg=COR_FUNDO_CARD, fg=COR_TEXTO
            ).pack()
        else:
            for i, jogador in enumerate(ordenado[:10], start=1):
                tk.Label(
                    card, text=f"{i}º - {jogador['nome']}: {jogador['pontos']} pontos",
                    font=FONTE_RANKING, bg=COR_FUNDO_CARD, fg=COR_TEXTO, anchor="w"
                ).pack(fill="x", pady=2)

        self.botao(self.root, "Voltar", self.tela_nome).pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizCopaApp(root)
    root.mainloop()
