CREATE TABLE LABDATABASE.SOCIOS (
                ID_SOCIO INTEGER NOT NULL,
                ENDERECO VARCHAR(200) NOT NULL,
                CPF VARCHAR(11) NOT NULL,
                NOME VARCHAR(100) NOT NULL,
                DATA_DESATIVACAO DATE,
                DATA_ASSOCIACAO DATE NOT NULL,
                EMAIL VARCHAR(100) NOT NULL,

)

CREATE TABLE LABDATABASE.PLANO (
                ID_PLANO INTEGER NOT NULL,
                ID_SOCIO INTEGER NOT NULL,
                NOME_PLANO VARCHAR(100) NOT NULL,
                VALOR FLOAT NOT NULL,

)

CREATE TABLE LABDATABASE.MENSALIDADE (
                ID_MENSALIDADE INTEGER NOT NULL,
                ID_PLANO  INTEGER NOT NULL,
                DATA_CRIACAO DATE NOT NULL,
                DATA_VENCIMENTO DATE NOT NULL,
                VALOR_COBRANCA FLOAT NOT NULL,
                MULTA FLOAT
)


