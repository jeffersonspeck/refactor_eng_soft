# Relatório de Refatoração e Qualidade de Código

## 1. Contextualização

Este relatório consolida os resultados da inspeção estática realizada sobre o script **`crawler-pokemon.py`** (anexo). A análise foi orientada pelos conceitos de **code smells** e **refactorings** descritos no *catálogo de Fowler* (cap. 9 do livro **Engenharia de Software Moderna**) e fundamentada em boas práticas de design de software.

---

## 2. Refactorings do Catálogo de Fowler (cap. 9)

* **Extração de Método (Extract Method)**
* **Inline de Método (Inline Method)**
* **Extração de Classe (Extract Class)**
* **Renomeação (Rename)**
* Outros Refactorings relevantes:

  * **Extração de Variável (Extract Variable)**
  * **Remoção de Flags (Remove Flag Argument)**
  * **Substituição de Condicional por Polimorfismo (Replace Conditional with Polymorphism)**
  * **Remoção de Código Morto (Remove Dead Code)**

---

## 3. Code Smells mais Frequentes

* **Código Duplicado (Duplicated Code)**
* **Métodos Longos (Long Method)**
* **Classes Grandes (Large Class)**
* **Feature Envy**
* **Métodos com Muitos Parâmetros (Long Parameter List)**
* **Variáveis Globais (Global Variables)**
* **Obsessão por Tipos Primitivos (Primitive Obsession)**
* **Objetos Mutáveis Excessivos (Mutable Data)**
* **Classes de Dados (Data Class)**
* **Comentários em Excesso ou Ausentes (Comment Smell)**

> **Nota ➀** — “Falta de verificação de nulos” não consta formalmente no catálogo de smells, mas foi incluída aqui por ser recorrente em sistemas Python que realizam *web scraping*.

---

## 4. Escopo do Relatório

O documento apresenta, para o trecho de código avaliado:

1. **Code smells identificados**;
2. **Refactorings aplicados ou recomendados**;
3. **Design patterns identificados ou sugeridos**.

---

## 5. Síntese dos Code Smells Identificados

| Code Smell                        | Trecho de Código (arquivo)                                | Refactoring Sugerido                                                                                                         | Comentários                                                                    |
| --------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Comentários Insuficientes         | Vários pontos sem explicação contextual                   | `Add Meaningful Comments` (Extrair documentos auxiliares)                                                                    | Falta de documentação prejudica manutenção e onboarding de novos devs.         |
| **Método Longo**                  | Função `crawl_page`                                       | **Extract Method** → separar lógica de (1) busca HTTP, (2) parsing, (3) validação & tratamento de exceções, (4) persistência | Garante adesão ao *Single Responsibility Principle*.                           |
| **Código Duplicado**              | Padrão de acesso a dados HTML duplicado em vários *loops* | `Extract Method` ou `Template Method`                                                                                        | Reduz repetição e facilita correção de bugs.                                   |
| **Obsessão por Tipos Primitivos** | Uso de `dict` para representar um Pokémon                 | **Extract Class → `Pokemon`**                                                                                                | Encapsula atributos, permite validações, métodos de domínio e garante tipagem. |
| Falta de verificação de nulos (➀) | `table.find(...).img.get(...)`                            | Criar **Guard Clauses** ou `Extract Method` de validação                                                                     | Previne lançamentos de `AttributeError` em tempo de execução.                  |

---

## 6. Refactorings Aplicados / Recomendados

As refatorações abaixo foram incorporadas (ou encontram‑se implantadas na versão refatorada enviada):

| Refactoring                   | Justificativa                                                         | Status          |
| ----------------------------- | --------------------------------------------------------------------- | --------------- |
| Extract Method                | Reduziu o tamanho da função `crawl_page` dividindo responsabilidades. | **Aplicado**    |
| Extract Class (`Pokemon`)     | Substituiu dicionários anônimos por objeto de domínio.                | **Recomendado** |
| Rename (`ix` → `table_index`) | Melhor legibilidade.                                                  | **Aplicado**    |
| Remove Dead Code              | Eliminação de variáveis não usadas e *imports* redundantes.           | **Aplicado**    |
| Extract Variable              | Melhoria na expressão de intenções dentro dos *if* aninhados.         | **Aplicado**    |

---

## 7. Design Patterns Identificados ou Sugeridos

| Padrão              | Ocorrência / Proposta                                                                                                     | Benefício                                                                            |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| **Template Method** | Generalização do fluxo de *scraping*: método abstrato `crawl_page()` e subclasses/variações caso o layout de página mude. | Evita código duplicado ao lidar com múltiplas páginas HTML com estrutura semelhante. |
| **Builder**         | Sugerido para compor objetos `Pokemon` passo a passo (id, nome, tipos, imagem).                                           | Facilita criação de objetos complexos com validações internas.                       |
| **Facade**          | Função de alto nível `run_crawler()` concentra configuração, chamadas de rede e persistência, abstraindo detalhes.        | Simplifica uso de todo o módulo por clientes externos.                               |

---

## 8. Próximos Passos

1. Implementar a classe **`Pokemon`** e, opcionalmente, um **`PokemonBuilder`**;
2. Extrair camada de serviço (por exemplo, `PokemonCrawler`) para encapsular política de *retry* e *rate‑limit*;
3. Cobrir refatorações com **testes unitários** (pytest) garantindo não regressão;
4. Documentar **exceções customizadas** para falhas de parsing;
5. Executar **linters** (`ruff`, `pylint`) e ferramentas de *static analysis* para monitorar novos smells.

---

## 9. Referências

* FOWLER, M. **Refactoring – Improving the Design of Existing Code**. Addison‑Wesley, 2019.
* SOMMERVILLE, I.; MUNNS, M. **Engenharia de Software Moderna**. Capítulo 9 – Refatoração de Código.
* GAMMA, E. *et al.* **Design Patterns: Elements of Reusable Object‑Oriented Software**.
