class Planos:
    def __init__(self,
                 id_plano: int = None,
                 nome_plano: str = None,
                 valor_plano: int = None
                 ):
        self.set_id_plano(id_plano)
        self.set_nome_plano(nome_plano)
        self.set_valor_plano(valor_plano)
    
    def set_id_plano(self, id_plano: int):
        self.id_plano = id_plano
    
    def set_nome_plano(self, nome_plano: str):
        self.nome_plano = nome_plano

    def set_valor_plano(self, valor_plano: int):
        self.valor_plano = valor_plano

    def get_id_plano(self) -> int:
        return self.id_plano

    def get_nome_plano(self) -> str:
        return self.nome_plano

    def get_valor_plano(self) -> int:
        return self.valor_plano

    def to_string(self) -> str:
        return f"ID: {self.id_plano} | Plano: {self.get_nome_plano()} | Valor: {self.get_valor_plano()}"
