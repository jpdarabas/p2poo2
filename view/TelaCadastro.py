import tkinter as tk
from tkinter import messagebox

class TelaCadastro(tk.Frame):
    def __init__(self, master, trocar_tela):
        super().__init__(master)
        self.gerenciador = master.gerenciador

        self.container = tk.Frame(self)
        self.container.pack(pady=10, expand=True)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.container, text="").pack(pady=30)
        tk.Label(self.container, text="Cadastro", font=("Arial", 36)).pack(pady=30)

        tk.Label(self.container, text="Usuario", font=("Arial", 16)).pack()
        self.usuario_entry = tk.Entry(self.container, width=30, font=("Arial", 12))
        self.usuario_entry.pack(pady=5)

        tk.Label(self.container, text="Senha", font=("Arial", 16)).pack()
        self.senha_entry = tk.Entry(self.container, show="*", width=30, font=("Arial", 12))
        self.senha_entry.pack(pady=5)

        tk.Label(self.container, text="Chave API", font=("Arial", 16)).pack()
        self.chave_entry = tk.Entry(self.container, show="*", width=30, font=("Arial", 12))
        self.chave_entry.pack(pady=5)
        tk.Button(self.container, text="Ajuda", command=lambda: messagebox.showinfo("Chave API TMDB", "Você pode obter uma gratuitamente registrando-se em https://www.themoviedb.org/signup e, em seguida, solicitando uma chave de API para desenvolvedores em https://www.themoviedb.org/settings/api"), font=("Arial", 12)).pack(pady=5)

        tk.Button(self.container, text="Cadastrar", command=self.cadastrar_usuario, font=("Arial", 16)).pack(pady=10)
        tk.Button(self.container, text="Cancelar", command=lambda: self.trocar_tela("TelaLogin"), font=("Arial", 16)).pack()


    def limpar_campos(self):
            self.usuario_entry.delete(0, tk.END)
            self.senha_entry.delete(0, tk.END)
            self.chave_entry.delete(0, tk.END)

    def trocar_tela(self, nome_tela):
        self.limpar_campos()
        self.master.trocar_tela(nome_tela)

    def cadastrar_usuario(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()
        chave_api = self.chave_entry.get()

        try:
            self.gerenciador.cadastrar_usuario(usuario, senha, chave_api)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.trocar_tela("TelaLogin")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {e}")