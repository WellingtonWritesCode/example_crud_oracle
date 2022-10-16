SELECT P.nome, count(*) as qtd_socios
FROM PLANOS P
GROUP BY P.nome;