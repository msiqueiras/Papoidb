# Projeto de Banco de Dados II - Papoidb

Esse repositório é o projeto da disciplina de Banco de Dados II, ministrada em 2026.4.

O objetivo da disciplina é construir um minidb em que se pode executar um `SELECT` com `WHERE`, de ponta a ponta (do parser ao disco), compreendendo a arquitetura interna de um SGBD.

Devido ao escopo do semestre, o projeto foi focado em entregar o **Mínimo Viável (M1 a M4)** funcional, além da implementação de um tópico da Parte 2 (Trabalho Final).

## Organização do projeto

O projeto está sendo desenvolvido em módulos ordenados, contendo um tema cada um.

* M1: Página e arquivo de dados
* M2: Cache de páginas (Buffer Pool)
* M3: Árvore B+, busca e inserção
* M4: Parser e catálogo

### Trabalho Final (Parte 2):
Tópico 1 - Executor e filtro: Implementação de `WHERE` simples no executor.

A construção é baseada na linguagem **Python**, utilizando a biblioteca `struct`/`bytearray` para manipulação binária e `poetry` para gerenciamento de dependências. O repositório contém um arquivo `NOTES.md` documentando as decisões de projeto e trade-offs de cada módulo.

## Estrura do projeto: 

```
.
├── .gitignore
├── NOTES.md
├── poetry.lock
├── pyproject.toml
├── README.md
|
├── images/
│   └── papoi.jpg
|
├── src/
│   ├── FileManager.py
│   ├── Page.py
│   ├── BufferPool.py
│   └── ...
|
└── tests/
    ├── m1_testes.ipynb
    ├── m2_testes.ipynb
    └── ...
```

## Etapa de implementação

- [x] M1
- [ ] M2
- [ ] M3
- [ ] M4

## Discentes

* João Vitor Martins Ferreira Maia - 202511140030
* Maria Luiza Rodrigues Siqueira - 202511140013


![Imagem de um personagem amarelo com o título "papoi" (minion)](images/papoi.jpg)