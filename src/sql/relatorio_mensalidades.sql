SELECT S.NOME AS NOME_SOCIO, DATA_CRIACAO, DATA_VENCIMENTO, DATA_PAGAMENTO, VALOR_COBRANCA, MULTA
FROM SOCIOS S, MENSALIDADES M
WHERE S.CPF = M.CPF