from models import GerenciaApp
import tkinter as tk
from view import *

class Main(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pesquisa de Filmes")
        self.state('zoomed')

        self.gerenciador = GerenciaApp()
        self.gerenciador.conectar()
        self.gerenciador.criar_tabela()

        self.frames = {}
        for F in (TelaLogin, TelaCadastro, TelaPrincipal):
            frame = F(self, self.trocar_tela)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.trocar_tela("TelaLogin")
        


    def trocar_tela(self, nome_tela):
        self.frames["TelaPrincipal"].atualizar_tela()
        frame = self.frames[nome_tela]
        frame.tkraise()


if __name__ == "__main__":
    main_app = Main()
    main_app.mainloop()