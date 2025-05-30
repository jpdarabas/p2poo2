import tkinter as tk
from tkinter import messagebox

class TelaLogin(tk.Frame):
    def __init__(self, master, trocar_tela):
        super().__init__(master)
        self.gerenciador = master.gerenciador

        self.container = tk.Frame(self)
        self.container.pack(pady=10, expand=True)

        tk.Label(self.container, text="").pack(pady=50)
        tk.Label(self.container, text="Login", font=("Arial", 36)).pack(pady=30)

        tk.Label(self.container, text="Usuario", font=("Arial", 16)).pack()
        self.usuario_entry = tk.Entry(self.container, width=30, font=("Arial", 12))
        self.usuario_entry.pack(pady=5)

        tk.Label(self.container, text="Senha", font=("Arial", 16)).pack()
        self.senha_entry = tk.Entry(self.container, show="*", width=30, font=("Arial", 12))
        self.senha_entry.pack(pady=5)

        tk.Button(self.container, text="Entrar", command=self.autenticar_usuario, font=("Arial", 16)).pack(pady=10)
        tk.Button(self.container, text="Cadastrar", command=lambda: self.trocar_tela("TelaCadastro"), font=("Arial", 16)).pack()

    def limpar_campos(self):
            self.usuario_entry.delete(0, tk.END)
            self.senha_entry.delete(0, tk.END)

    def trocar_tela(self, nome_tela):
        self.limpar_campos()
        self.master.trocar_tela(nome_tela)

    def autenticar_usuario(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()

        try:
            if self.gerenciador.login(usuario, senha):
                self.trocar_tela("TelaPrincipal")
            else:
                messagebox.showerror("Erro", "Usuário ou senha inválidos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao autenticar usuário: {e}")