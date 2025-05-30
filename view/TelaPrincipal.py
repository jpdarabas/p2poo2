import tkinter as tk
from tkinter import messagebox
from models import *

class TelaPrincipal(tk.Frame):
    def __init__(self, master, trocar_tela):
        super().__init__(master)
        self.master = master
        self.gerenciador: GerenciaApp = master.gerenciador
        self.trocar_tela = trocar_tela
        # Container que será atualizado dinamicamente
        self.container = tk.Frame(self)
        self.container.pack(pady=10, expand=True)

        # Botão sair
        self.botao_sair = tk.Button(self, text="Sair", command=lambda: trocar_tela("TelaLogin"))
        self.botao_sair.pack(pady=10)

        self.__filtro_nome = ""
        self.__filtro_genero = ""
        self.__filtro_data_inicial = ""
        self.__filtro_data_final = ""
        self.__pagina_atual = 1

        self.atualizar_tela()


    def atualizar_tela(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        usuario = self.gerenciador.get_usuario()
        if usuario:
            tk.Label(self.container, text=f"Bem-vindo, {usuario.get_nome()}!", font=("Arial", 16)).pack(pady=10)

        # Frame com filtros
        filtros_frame = tk.Frame(self.container)
        filtros_frame.pack(pady=10)

        tk.Label(filtros_frame, text="Nome:").grid(row=0, column=0, padx=5)
        self.entry_nome = tk.Entry(filtros_frame, width=20)
        self.entry_nome.insert(0, self.__filtro_nome)
        self.entry_nome.grid(row=0, column=1, padx=5)

        tk.Label(filtros_frame, text="Gênero:").grid(row=0, column=2, padx=5)
        self.entry_genero = tk.Entry(filtros_frame, width=15)
        self.entry_genero.insert(0, self.__filtro_genero)
        self.entry_genero.grid(row=0, column=3, padx=5)

        tk.Label(filtros_frame, text="Data Inicial:").grid(row=0, column=4, padx=5)
        self.entry_data_inicial = tk.Entry(filtros_frame, width=12)
        self.entry_data_inicial.insert(0, self.__filtro_data_inicial)
        self.entry_data_inicial.grid(row=0, column=5, padx=5)

        tk.Label(filtros_frame, text="Data Final:").grid(row=0, column=6, padx=5)
        self.entry_data_final = tk.Entry(filtros_frame, width=12)
        self.entry_data_final.insert(0, self.__filtro_data_final)
        self.entry_data_final.grid(row=0, column=7, padx=5)

        tk.Button(filtros_frame, text="Filtrar", width=10, command=self.filtrar_filmes).grid(row=0, column=8, padx=10)

        tk.Button(filtros_frame, text="Limpar Filtros", width=15, command=self.limpar_filtros).grid(row=0, column=9, padx=10)

        filmes = self.gerenciador.get_filmes()
        for filme in filmes:
            filme_frame = tk.Frame(self.container)
            filme_frame.pack(pady=5, anchor="w", fill="x")

            tk.Label(filme_frame, text=f"{filme.get_titulo()} ({filme.get_data_lancamento().split('-')[0]})", font=("Arial", 14)).grid(row=0, column=0, padx=5)

            tk.Label(filme_frame, text=f"Gêneros: {', '.join(filme.get_generos())}", font=("Arial", 12)).grid(row=0, column=1, padx=5)

            tk.Label(filme_frame, text=f"Nota: {filme.get_nota() if filme.get_n_avaliacoes() > 0 else 'Não Avaliado'}", font=("Arial", 12)).grid(row=0, column=2, padx=5)
            tk.Label(filme_frame, text=f"Nº Avaliações: {filme.get_n_avaliacoes()}", font=("Arial", 12)).grid(row=0, column=3, padx=5)
            tk.Button(
                filme_frame,
                text="Ver Detalhes",
                command=lambda f=filme: self.mostrar_info(
    f.get_titulo(),
    f"Data de Lançamento: {self.gerenciador.formatar_data(f.get_data_lancamento())}\n\n{f'Sinopse: {f.get_sinopse()}' if f.get_sinopse() != '' else 'Sinopse não disponível.'}"
),
                font=("Arial", 11)
            ).grid(row=0, column=4, padx=5)

        frame_paginacao = tk.Frame(self.container)
        frame_paginacao.pack(pady=10)


        for i in range(1, min(10, self.gerenciador.get_paginas()) + 1):
            botao_pagina = tk.Button(frame_paginacao, text=str(i), command=lambda pagina=i: self.trocar_pagina(pagina), font=("Arial", (14 if i == self.__pagina_atual else 10)))
            botao_pagina.pack(side="left", padx=5)

    def mostrar_info(self, titulo, texto):
        janela = tk.Toplevel()
        janela.title(titulo)
        
        tk.Label(janela, text=texto, font=("Arial", 14), wraplength=400, justify="left").pack(padx=20, pady=20)
        tk.Button(janela, text="OK", command=janela.destroy, font=("Arial", 12)).pack(pady=10)


    def filtrar_filmes(self, pagina=1):
        self.__pagina_atual = pagina
        self.__filtro_nome = self.entry_nome.get().strip().lower()
        self.__filtro_genero = self.entry_genero.get().strip().lower()
        self.__filtro_data_inicial = self.entry_data_inicial.get().strip()
        self.__filtro_data_final = self.entry_data_final.get().strip()

        if self.__filtro_nome == "":
            self.__filtro_nome = None
        if self.__filtro_genero == "":
            self.__filtro_genero = None
        else:
            try:
                self.__filtro_genero = self.gerenciador.genero_to_id(self.__filtro_genero.capitalize())
            except ValueError:
                messagebox.showerror("Erro", "Gênero inválido.")
                return
        if self.__filtro_data_inicial == "":
            self.__filtro_data_inicial = None
        else:
            self.__filtro_data_inicial = self.gerenciador.desformatar_data(self.__filtro_data_inicial)
            if self.__filtro_data_inicial is None:
                messagebox.showerror("Erro", f"Formato de data inválido: {self.entry_data_inicial.get().strip()}. Use o formato DD/MM/AAAA.")
                return
        if self.__filtro_data_final == "":
            self.__filtro_data_final = None
        else:
            self.__filtro_data_final = self.gerenciador.desformatar_data(self.__filtro_data_final)
            if self.__filtro_data_final is None:
                messagebox.showerror("Erro", f"Formato de data inválido: {self.entry_data_final.get().strip()}. Use o formato DD/MM/AAAA.")
                return

        try:
            self.gerenciador.buscar_filmes(nome=self.__filtro_nome, genero=self.__filtro_genero, data_inicial=self.__filtro_data_inicial, data_final=self.__filtro_data_final, pagina=pagina)
            self.limpar_filtros(manter=True)
            self.atualizar_tela()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar filmes: {e}")
            return

    def limpar_filtros(self, manter=False):
        if not manter:
            self.__filtro_nome = ""
            self.__filtro_genero = ""
            self.__filtro_data_inicial = ""
            self.__filtro_data_final = ""
        else:
            if self.__filtro_nome == None:
                self.__filtro_nome = ""
            if self.__filtro_genero == None:
                self.__filtro_genero = ""
            else:
                self.__filtro_genero = self.gerenciador.id_to_genero(self.__filtro_genero)
            if self.__filtro_data_inicial == None:
                self.__filtro_data_inicial = ""
            else:
                self.__filtro_data_inicial = self.gerenciador.formatar_data(self.__filtro_data_inicial)
            if self.__filtro_data_final == None:
                self.__filtro_data_final = ""
            else:
                self.__filtro_data_final = self.gerenciador.formatar_data(self.__filtro_data_final)
            

        self.entry_nome.delete(0, tk.END)
        self.entry_genero.delete(0, tk.END)
        self.entry_data_inicial.delete(0, tk.END)
        self.entry_data_final.delete(0, tk.END)
        
    def trocar_pagina(self, pagina):
        try:
            self.__pagina_atual = pagina
            self.filtrar_filmes(pagina)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao trocar de página: {e}")