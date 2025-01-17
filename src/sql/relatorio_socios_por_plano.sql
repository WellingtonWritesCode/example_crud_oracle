SELECT NOME_PLANO, COUNT(*) QTD_SOCIOS
FROM(
    SELECT P.NOME AS NOME_PLANO, S.ID_PLANO AS QTD_SOCIOS FROM PLANOS P
    INNER JOIN SOCIOS S
    ON P.ID_PLANO = S.ID_PLANO
)
GROUP BY NOME_PLANO