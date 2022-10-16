class Planos:
    def __init__(self,

                 nome_plano: str = None,
                 valor_plano: int = None
                 ):

        self.set_nome_plano(nome_plano)
        self.set_valor_plano(valor_plano)

    def set_nome_plano(self, nome_plano: str):
        self.nome_plano = nome_plano

    def set_valor_plano(self, valor_plano: int):
        self.valor_plano = valor_plano

    def get_nome_plano(self) -> str:
        return self.nome_plano

    def get_valor_plano(self) -> int:
        return self.valor_plano

    def to_string(self) -> str:
        return f"Plano: {self.get_nome_plano()} | Valor: {self.get_valor_plano()}"
