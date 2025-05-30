class Usuario():
    def __init__(self, 
    id:int | None,
    usuario:str,
    ):
        self.__id = id
        self.__usuario = usuario

    # Getters
    def get_id(self):
        return self.__id

    def get_nome(self):
        return self.__usuario

    # Setters
    def set_id(self, id):
        self.__id = id

    def set_nome(self, usuario):
        self.__usuario = usuario
    