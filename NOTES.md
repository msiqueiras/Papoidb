# Módulo 1

O tipo padrão `bytes` em Python é IMUTÁVEL. A função `le_pagina` precisa retornar um `bytearray` em todas as situações para que o objeto se comporte como uma lista modificável na memória RAM. A decisão mais difícil nessa função foi o tratamento, já que o minidb exige que todos os vetores possuam o mesmo tamanho de 4096.