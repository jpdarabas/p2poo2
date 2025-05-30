from models.Usuario import Usuario
from models.Filme import Filme
import sqlite3
import requests
from utils.generos import generos

class GerenciaApp():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GerenciaApp, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_inicializado") and self._inicializado:
            return
        self._inicializado:bool = True
        self.nome_banco:str = "usuarios.db"
        self.__conexao = None
        self.__usuario: Usuario | None = None
        self.__filmes: list[Filme] = []
        self.__chave_api: str | None = None
        self.__paginas: int = 1
        

    def conectar(self):
        self.__conexao = sqlite3.connect(self.nome_banco)
        self.__conexao.row_factory = sqlite3.Row
        self.__cursor = self.__conexao.cursor()
        self.__conexao.execute("PRAGMA foreign_keys = ON")

    def desconectar(self):
        if self.__cursor:
            self.__cursor.close()
        if self.__conexao:
            self.__conexao.close()

    def criar_tabela(self):
        if not self.__conexao:
            self.conectar()

        with open("utils/usuarios.sql", 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        self.__cursor.execute(sql_script)
        
        self.__conexao.commit()

    ## USUÁRIOS ##

    # Getter
    def get_usuario(self):
        return self.__usuario

    # Cadastro Usuário
    def cadastrar_usuario(self, usuario, senha, chave_api):
        if not self.__conexao or not self.__cursor:
            self.conectar()

        if not chave_api:
            raise ValueError("Chave API não pode ser vazia.")
        
        if not usuario or not senha:
            raise ValueError("Usuário e senha não podem ser vazios.")
        elif usuario == senha:
            raise ValueError("Usuário e senha não podem ser iguais.")

        self.__chave_api = chave_api
        self.buscar_filmes()
        if self.__filmes == []:
            raise ValueError(f"Chave inválida")
            
        
        self.__cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
        self.__conexao.commit()
        id_usuario = self.__cursor.lastrowid
        with open("utils/chaves.txt", "a", encoding="utf-8") as f:
                f.write(f"{id_usuario}:{chave_api}\n")

    # Login
    def login(self, usuario, senha):
        try:
            if not self.__conexao:
                self.conectar()

            self.__cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
            usuario = self.__cursor.fetchone()
            if usuario:
                self.__usuario = Usuario(usuario["id"], usuario["usuario"])
                try:
                    self.__chave_api = self.carregar_chave_api(self.__usuario.get_id())
                except Exception as e:
                    print(f"Erro ao carregar chave da API: {e}")
                    self.__chave_api = None
                    raise ValueError("Chave API não encontrada ou inválida.")
                print(f"Usuário {self.__usuario.get_nome()} logado com sucesso.")
                self.buscar_filmes()
                return True
            return False
        except Exception as e:
            print(f"Erro no login: {e}")
            raise
    

    def carregar_chave_api(self, id_usuario, caminho="utils/chaves.txt"):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                for linha in f:
                    user_id, chave = linha.strip().split(":", 1)
                    if int(user_id) == int(id_usuario):
                        return chave
        except FileNotFoundError:
            raise

    def buscar_filmes(self, nome=None, genero=None, data_inicial=None, data_final=None, pagina=1):
        url = 'https://api.themoviedb.org/3/discover/movie'
        params = {
            'api_key': self.__chave_api,
            'language': 'pt-BR',
            'sort_by': 'popularity.desc',
            'include_adult': 'false',
            'include_video': 'false',
            'page': pagina
        }
        if nome:
            url = 'https://api.themoviedb.org/3/search/movie'
            params['query'] = nome
            if genero or data_inicial or data_final:
                raise ValueError("Se 'nome' for fornecido, 'genero', 'data_inicial' e 'data_final' não devem ser usados.")
        if genero:
            params['with_genres'] = genero
        if data_inicial:
            params['primary_release_date.gte'] = data_inicial
        if data_final:
            params['primary_release_date.lte'] = data_final

        resposta = requests.get(url, params=params)
        if resposta.status_code != 200:
            print(resposta.json())
            print(self.__chave_api)

        resultados = resposta.json().get('results', [])
        self.__paginas = resposta.json().get('total_pages', 1)
        

        self.__filmes = [Filme(
            titulo=filme.get('title'),
            generos=[self.id_to_genero(g) for g in filme.get('genre_ids', [])],
            data_lancamento=filme.get('release_date'),
            sinopse=filme.get('overview'),
            nota=filme.get('vote_average'),
            n_avaliacoes=filme.get('vote_count')
        ) for filme in resultados]


    def id_to_genero(self, genero_id):
        for genero in generos:
            if genero['id'] == genero_id:
                return genero['name']
        return "Desconhecido"
    
    def genero_to_id(self, genero_nome):
        for genero in generos:
            if genero['name'].lower() == genero_nome.lower():
                return genero['id']
        return None

    def formatar_data(self, data):
        if not data:
            return None
        partes = data.split('-')
        if len(partes) != 3:
            return None
        ano, mes, dia = partes
        return f"{dia}/{mes}/{ano}"
    
    def formatar_data(self, data):
        if not data:
            return None
        partes = data.split('-')
        if len(partes) != 3:
            return None
        ano, mes, dia = partes
        return f"{dia}/{mes}/{ano}"
    
    def desformatar_data(self, data):
        if not data:
            return None
        partes = data.split('/')
        if len(partes) != 3:
            return None
        dia, mes, ano = partes
        if not (dia.isdigit() and mes.isdigit() and ano.isdigit()):
            return None
        return f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"

    # Getters
    def get_filmes(self):
        return self.__filmes

    def get_paginas(self):
        return self.__paginas
    
    def get_usuario(self):
        return self.__usuario