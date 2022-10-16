CREATE TABLE LABDATABASE.SOCIO( 
                ID_SOCIO INTEGER NOT NULL,
                NOME VARCHAR2(100) NOT NULL,
                EMAIL VARCHAR2(100) NOT NULL,
                CPF VARCHAR2(11) NOT NULL,
                ENDERECO VARCHAR2(200) NOT NULL,
                DATA_DESATIVACAO DATE,
                DATA_ASSOCIACAO DATE  NOT NULL,
                CONSTRAINT SOCIO_pk PRIMARY KEY(ID_SOCIO) 
);

CREATE TABLE LABDATABASE.PLANO( 
                ID_PLANO INTEGER NOT NULL,
                ID_SOCIO INTEGER NOT NULL,
                NOME_PLANO VARCHAR2(100) NOT NULL,
                VALOR FLOAT NOT NULL,
                CONSTRAINT PLANO_pk PRIMARY KEY(ID_PLANO)
);

CREATE TABLE LABDATABASE.MENSALIDADE(
                ID_MENSALIDADE INTEGER NOT NULL,
                ID_PLANO INTEGER NOT NULL,
                DATA_CRIACAO DATE NOT NULL,
                DATA_VENCIMENTO  DATE NOT NULL,
                VALOR_COBRANCA FLOAT NOT NULL,
                MULTA FLOAT
                CONSTRAINT MENSALIDADE_pk PRIMARY KEY (ID_MENSALIDADE)
);

ALTER TABLE PLANOS ADD CONSTRAINT SOCIOS_PLANO_fk FOREIGN KEY (ID_SOCIO) REFERENCES SOCIOS (ID_SOCIO);

ALTER TABLE MENSALIDADE ADD CONSTRAINT PLANO_MENSALIDADE_fk FOREIGN KEY(ID_PLANO) REFERENCES PLANO(ID_PLANO); 

ALTER TABLE MENSALIDADE ADD CONSTRAINT SOCIO_MENSALIDADE_fk FOREIGN KEY(ID_PLANO) REFERENCES SOCIO(ID_SOCIO);