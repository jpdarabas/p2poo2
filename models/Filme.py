class Filme():
    def __init__(self, 
                 titulo:str, 
                 generos:list[str], 
                 data_lancamento:str,
                 sinopse:str, 
                 nota:float,
                 n_avaliacoes:int):
        self.__titulo = titulo
        self.__generos = generos
        self.__data_lancamento = data_lancamento
        self.__sinopse = sinopse
        self.__nota = nota
        self.__n_avaliacoes = n_avaliacoes

    # Getters
    def get_titulo(self):
        return self.__titulo
    def get_generos(self):
        return self.__generos
    def get_data_lancamento(self):
        return self.__data_lancamento
    def get_nota(self):
        return self.__nota
    def get_sinopse(self):
        return self.__sinopse
    def get_n_avaliacoes(self):
        return self.__n_avaliacoes