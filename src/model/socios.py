class Socios:
    def __init__(self,
                 CPF: str = None,
                 id_plano: int = None,
                 endereco: str = None,
                 nome: str = None,
                 data_associacao: str = None,
                 data_desativacao: str = None,
                 telefone: str = None,
                 email: str = None
                 ):

        self.set_CPF(CPF)
        self.set_id_plano(id_plano)
        self.set_endereco(endereco)
        self.set_nome(nome)
        self.set_data_associacao(data_associacao)
        self.set_data_desativacao(data_desativacao)
        self.set_telefone(telefone)
        self.set_email(email)

    def set_CPF(self, CPF: str):
        self.CPF = CPF

    def set_id_plano(self, id_plano: int):
        self.id_plano = id_plano

    def set_endereco(self, endereco: str):
        self.endereco = endereco

    def set_nome(self, nome: str):
        self.nome = nome

    def set_data_associacao(self, data_assosiacao: str):
        self.data_associacao = str(data_assosiacao)[:10]

    def set_data_desativacao(self, data_desativacao: str):
        self.data_desativacao = str(data_desativacao)[:10]

    def set_telefone(self, telefone: str):
        self.telefone = telefone

    def set_email(self, email: str):
        self.email = email

    def get_CPF(self) -> str:
        return self.CPF

    def get_id_plano(self) -> int:
        return self.id_plano

    def get_endereco(self) -> str:
        return self.endereco

    def get_nome(self) -> str:
        return self.nome

    def get_data_associacao(self) -> str:
        return self.data_associacao

    def get_data_desativacao(self) -> str:
        return self.data_desativacao

    def get_telefone(self) -> str:
        return self.telefone

    def get_email(self) -> str:
        return self.email

    def to_string(self) -> str:
        return (f"CPF: {self.get_CPF()} | {self.get_id_plano()}\n"+
                f"{self.get_endereco()}\n"+
                f"{self.get_nome()} | {self.get_data_associacao()} | {self.get_data_desativacao()}\n"+
                f"{self.get_telefone()} | {self.get_email()}")
