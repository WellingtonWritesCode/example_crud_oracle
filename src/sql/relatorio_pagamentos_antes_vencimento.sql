SELECT S.nome, M.data_pagamento FROM SOCIOS S
INNER JOIN MENSALIDADES M
on m.data_pagamento <= m.data_vencimento;