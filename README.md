# Projeto de Banco de Dados II - Papoidb

Esse repositório é o projeto da disciplina de Banco de Dados II, ministrada em 2026.4. O objetivo da disciplina é construir um minidb em que se pode executar um SELECT com WHERE, dentro de uma transação que volta ao ar consistente depois de um kill -9 no meio do commit

## Organização do projeto

O projeto está sendo desenvolvido em módulos ordenados, de 1 ao 7, contendo um tema cada um.

* M1: Página e arquivo de dados
* M2: Cache de páginas
* M3: Árvore B+, busca e inserção
* M4: Parser e catálogo
* M5: Executor: varredura sequencial por índice
* M6: Transações: BEGIN, COMMIT, ROLLBACK
* M7: Recuperação: log de escrita antecipada

A construção será baseada na linguagem Python e irá conter um arquivo NOTES.md para as decisões de cada módulo.

### Discentes

* João Vitor Martins Ferreira Maia - 202511140030
* Maria Luiza Rodrigues Siqueira - 202511140013
