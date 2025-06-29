# Relatório Técnico de Refatoração

*Projeto Pokémon Crawler – Comparativo entre Código Original e Versão Refatorada*

---

## Documentações auxiliares

1. [Manual de Configuração e Instalação](docs/install-ptBR.md)
2. [Documentação Técnica](docs/documentation-ptBR.md)
3. [Documentação Interativa](https://jeffersonspeck.github.io/refactor_eng_soft/)

## Sumário

1. [Links indicados pelo professor](#1-links-indicados-pelo-professor)
2. [Visão geral da nova arquitetura](#2-visão-geral-da-nova-arquitetura)
3. [Principais melhorias em relação ao código original](#3-principais-melhorias-em-relação-ao-código-original)
4. [Design patterns identificados / aplicados](#4-design-patterns-identificados--aplicados)
5. [Code smells & refactorings](#5-code-smells--refactorings)
6. [Pontos fortes da nova solução](#6-pontos-fortes-da-nova-solução)
7. [Oportunidades de melhoria e próximos passos](#7-oportunidades-de-melhoria-e-próximos-passos)
8. [Contextualização e fundamentação teórica](#8-contextualização-e-fundamentação-teórica)
9. [Referências](#9-referências)

---

## Bibliografia

| Descrição            | URL |
| -------------------- | --- |
| Leitura indicada     | [Livro](https://engsoftmoderna.info/cap9.html) |
| Página usada em aula | [URL](https://refactoring.guru/pt-br/refactoring/smells) |

---

## 1. Codes Smells

| Nº | Code Smell                                        | Descrição                                                                 |
|----|---------------------------------------------------|---------------------------------------------------------------------------|
| 1  | Código Duplicado                                  | Requisições e limpeza de HTML repetidas em diferentes pontos do código.  |
| 2  | Função Longa                                       | A função `crawl_page` realiza múltiplas tarefas sem modularização.       |
| 3  | Variável Global                                    | Uso de `pokemon_list` como variável global compartilhada.                |
| 4  | Captura Genérica de Exceções                      | Uso de `except Exception`, dificultando a identificação do erro real.    |
| 5  | Responsabilidades Misturadas                       | O bloco `__main__` combina lógica de rede, controle e persistência.      |
| 6  | Obsessão por Tipos Primitivos                     | Uso de dicionários (`dict`) em vez de objetos estruturados.              |
| 7  | Logging Insuficiente                              | Ausência de logs informativos durante o processamento.                   |
| 8  | Números e Strings Mágicas                         | Uso direto de valores fixos no código (ex.: cores e índices).            |
| 9  | Falta de Modularização                            | Ausência de funções auxiliares para dividir responsabilidades.           |
| 10 | Função Genérica Demais                            | `get_pages` retorna todos os links sem qualquer critério de filtragem.   |

---

## 2. Visão geral da nova arquitetura

```text
.
├── docs/            # documentações diversas do projeto
├── logs/            # arquivos .txt gerados pelo logger
├── models/          # entidades de domínio
│   ├── pokemon.py
│   └── pokemon_builder.py
├── services/        # regras de negócio e utilitários
│   ├── csv_writer.py        # escreve o csv
│   ├── csv_analyzer.py      # analiza a consistência
│   ├── logging.py           # configuração central de logs
│   ├── pokemon_crawler.py   # crawler e parser
│   └── quests.py            # utilidades extra (ex.: missões)
├── output/          # artefatos gerados (pokemons.csv)
├── olds/            # arquivos antigos antes da fatoração (originais do Prof. Sidgley)
└── main.py          # ponto de entrada do aplicativo
```

### 2.1 Principais diferenças estruturais

| **Aspecto**                | **Código Original (`crawler-pokemon.py`)** | **Código Refatorado**                                          | **Ganhos / Impacto**                                      |
| -------------------------- | ------------------------------------------ | -------------------------------------------------------------- | --------------------------------------------------------- |
| **Organização de pastas**  | Arquivo único                              | `models/`, `services/`, `logs/`, `output/`                     | Modularidade, escalabilidade, onboarding facilitado       |
| **Modelo de dados**        | `dict` genérico                            | `@dataclass Pokemon` (imutável)                                | Tipagem forte, segurança, legibilidade                    |
| **Criação de objetos**     | Lógica espalhada                           | Padrão *Builder* com `PokemonBuilder`                          | Validação progressiva, extensibilidade                    |
| **Parsing & Crawling**     | Função única longa (`crawl_page`)          | `PokemonCrawler` com métodos especializados (`fetch`, `parse`) | Redução de complexidade ciclomática, SRP¹, testabilidade  |
| **Logging**                | `logging.basicConfig` único                | `setup_logging()` com múltiplos handlers                       | Logs padronizados e reutilizáveis                         |
| **Tratamento de erros**    | `except Exception` genérico                | `ParsingError`, logs detalhados com `exc_info`                 | Depuração facilitada, rastreabilidade de falhas           |
| **Organização da saída**   | CSV na raiz do projeto                     | `output/pokemons.csv`                                          | Separação clara entre artefato e código                   |
| **Análise pós-crawl**      | Inexistente                                | `csv_analyzer.py`                                              | Checagem de consistência, estatísticas úteis              |
| **Exportação CSV**         | Ad-hoc inline                              | Função `write_pokemon_csv()` em `csv_writer.py`                | Reuso, clareza, responsabilidade única                    |
| **Extras / Narrativas**    | Inexistente                                | `quests.py` adiciona missões aleatórias                        | Valor educacional, gamificação opcional para visualização |
| **Preparação para testes** | Sem estrutura                              | Classes com responsabilidades únicas                           | Testes unitários via `pytest` viáveis e incentivados      |
> ¹ *SRP = Single Responsibility Principle (Princípio da Responsabilidade Única).*

### 2.2 BPMN

![BPMN](docs/pokemon.svg)

### 2.3 UML

![UML](docs/uml.svg)

---

## 3. Principais melhorias em relação ao código original

| Categoria                  | Melhoria Implementada                                                    | Impacto                                                                     |
| -------------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------- |
| **Arquitetura**            | Pastas lógicas (`models`, `services`, `logs`, `output`)                  | Facilita escalabilidade e onboarding de novos desenvolvedores               |
| **Domínio**                | `Pokemon` como `@dataclass` imutável                                     | Elimina “Obsessão por Tipos Primitivos”, garante consistência dos atributos |
| **Criação de Objetos**     | `PokemonBuilder` permite construção passo a passo com validações         | Evita construtores gigantes ou muitos parâmetros opcionais                  |
| **Parsing**                | Métodos especializados (`fetch_html`, `discover_pages`, `_parse_tables`) | Reduz complexidade ciclomática e duplicação                                 |
| **Logging**                | Configuração única (`logging.py`) + arquivo dedicado em `logs/`          | Logs mais legíveis, filtráveis e reutilizáveis                              |
| **CSV correcto**           | `Pokemon.to_dict()` padroniza ordem das colunas                          | Corrige desalinhamento que ocorria no original                              |
| **Análise**                | `csv_analyzer.py` realiza checagens de integridade e estatísticas        | Verifica duplicidades, valores nulos, distribuição de tipos                 |
| **Preparação para testes** | Cada classe tem responsabilidade única                                   | Facilita criação de suíte `pytest`                                          |

---

## 4. Design patterns identificados / aplicados

| Pattern                        | Local / Papel                                                                               |
| ------------------------------ | ------------------------------------------------------------------------------------------- |
| **Builder**                    | `PokemonBuilder` – criação de objetos complexos sem construtores gigantes.                  |
| **Facade / Utility**           | `PokemonCSVAnalyzer` – interface simplificada para inspeção de CSV.                         |
| **Factory Method (implícito)** | `PokemonCrawler.crawl()` – decide como instanciar `PokemonBuilder` conforme estrutura HTML. |
| **Singleton (implícito)**      | Configuração global de logger em `setup_logging()` – garante instância única de `Logger`.   |

---

## 5. Code smells & refactorings

### 5.1 Mapa geral de smells corrigidos

| Nº | Code Smell                        | Como foi resolvido no projeto refatorado                                                                                                                                                    |
| -- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1  | **Código Duplicado**              | Foi criado o método `fetch_html()` em `PokemonCrawler` e funções auxiliares em `main.py` (`discover_urls`, `crawl_all_pages`) – toda lógica de requisição/decodificação ficou centralizada. |
| 2  | **Função Longa**                  | A antiga `crawl_page` foi substituída por uma classe `PokemonCrawler` com métodos internos pequenos (`_parse_single_table`, `_maybe_extract_*`).                                            |
| 3  | **Variável Global**               | A lista global `pokemon_list` deixou de existir; cada chamada a `PokemonCrawler.crawl()` devolve uma lista que é agregada localmente em `main.py`.                                          |
| 4  | **Captura Genérica de Exceções**  | Nos módulos refatorados passaram-se a capturar exceções específicas (`URLError`, `HTTPError`, `AttributeError`, `IndexError`, `TypeError`, `FileNotFoundError`, etc.).                      |
| 5  | **Responsabilidades Misturadas**  | `main.py` foi modularizado: configuração de ambiente, descoberta de URLs, captura, escrita de CSV e análise ficam em funções separadas; a persistência (CSV) migrou para `csv_writer.py`.   |
| 6  | **Obsessão por Tipos Primitivos** | Introduzidos `Pokemon` (dataclass imutável) e `PokemonBuilder`; o crawler passa a devolver objetos estruturados em vez de `dict`.                                                           |
| 7  | **Logging Insuficiente**          | Implementado `services.logging.setup_logging()` (arquivo e console opcionais, níveis configuráveis); todos os módulos usam `logging` com mensagens informativas.                            |
| 8  | **Números e Strings Mágicas**     | Criada a enum‐lite `PokemonFields` em `pokemon_crawler.py`; constantes de cor e separadores estão declaradas em variáveis nomeadas.                                                         |
| 9  | **Falta de Modularização**        | Funções utilitárias (`clean_csv_value`, `is_effectively_empty`), builders, analisadores e quests foram extraídos para módulos próprios; cada responsabilidade ganhou um arquivo.            |
| 10 | **Função Genérica Demais**        | `get_pages` foi descartada; `discover_pages()` filtra links que começam por `/conteudo/pokemon/` e terminam em `.htm`, removendo duplicatas e ordenando.                                    |
> **Nota:** Algumas melhorias estruturais complementares também são consideradas refatorações válidas conforme Fowler (2019), mesmo sem alterar a lógica do programa. Entre elas:
> 
> - **Adicionar docstrings e comentários descritivos**, desde que aumentem a clareza e compreensão do código;
> - **Corrigir indentação, formatação e nomes ambíguos**, melhorando a legibilidade;
> - **Mover trechos de código entre arquivos** (por exemplo, extrair classes utilitárias para módulos separados), desde que preserve o comportamento e melhore a organização interna.

---

## 6. Pontos fortes da nova solução

1. **Separação clara de camadas** (domínio, serviços, aplicação).
2. **Alta coesão**: cada módulo faz apenas uma coisa.
3. **Logs acionáveis**: mensagens contextualizadas, facilitando troubleshooting.
4. **Exportação de dados confiável**: CSV gerado com colunas corretas e ordem estável.
5. **Pronto para testes unitários**: dependências mínimas e injeção fácil de mocks.
6. **Extensível a outros sites**: basta implementar novas estratégias de parsing.

---

## 7. Oportunidades de melhoria e próximos passos

| Tema                       | Ação Recomendada                                                                     |
| -------------------------- | ------------------------------------------------------------------------------------ |
| **Tipagem**                | Usar `pydantic` para validação de modelos ou `typing.Annotated`.                     |
| **Testes**                 | Implementar suíte `pytest` com cobertura de >80 %.                                   |
| **CI/CD**                  | Adicionar *pre-commit* (black, isort, ruff) e GitHub Actions.                        |
| **Pattern Strategy**       | Permitir crawlers para múltiplas fontes de dados Pokémon.                            |
| **Tratamento de exceções** | Trocar `except Exception` genérico por exceções específicas (`requests.exceptions`). |

---

## 8. Contextualização e fundamentação teórica

O processo de inspeção e refatoração tomou como base:

* **Catálogo de Fowler** – Cap. 9 do livro *Engenharia de Software Moderna* traz uma adaptação dos 11 refactorings essenciais (Extração de Método, Inline Method, Extração de Classe, etc.) e guidelines para aplicação incremental.
* **Catálogo de Code Smells** – Fowler (cap. 7) define sinais de código de baixa qualidade como *Long Method*, *Primitive Obsession*, *Duplicated Code* e outros.
* **Design Patterns (GoF)** – *Builder* e *Facade* foram empregados para reduzir acoplamento e expor APIs claras.

A refatoração conduzida elimina grande parte dos smells, melhora métricas de complexidade e prepara o projeto para evoluções (novos crawlers, persistência em banco de dados, API REST, etc.).

---

## 9. Referências

1. Fowler, M. **Refactoring: Improving the Design of Existing Code**. 2ª ed. Addison-Wesley, 2019.
2. Sommerville, I.; Munns, M. **Engenharia de Software Moderna**. Pearson, 2021 – Cap. 9 (Refatoração).
3. Gamma, E.; Helm, R.; Johnson, R.; Vlissides, J. **Design Patterns: Elements of Reusable Object-Oriented Software**. Addison-Wesley, 1994.
4. Docs oficiais – *Python Standard Library: logging*; *BeautifulSoup 4 Documentation*; *pandas User Guide*.

---

### Observação Final

Este documento foi elaborado para servir como documentação do trabalho de refatoração efetuado.

## Licença

Este projeto é disponibilizado para **uso acadêmico e educacional**, com permissão para:

- Usar livremente o código-fonte;
- Modificar e adaptar conforme necessário;
- Compartilhar versões modificadas.

**Condições de uso**:
- É obrigatório manter a **citação dos autores originais**.
- Em qualquer redistribuição ou adaptação, deve ser incluído crédito visível a:
  - [Edinéia dos Santos Brizola Brum](https://github.com/edibrum)  
  - [Jefferson Rodrigo Speck](https://github.com/jeffersonspeck)  
  - [Rafael Ferreira Lima](ferreira.rfl@gmail.com)
- A atividade foi originalmente proposta pelo professor [Sidgley Camargo de Andrade](https://github.com/sidgleyandrade), e isso também deve ser reconhecido nas versões derivadas.

Este projeto **não pode ser comercializado** nem utilizado com fins lucrativos.

---

## Autores

- [Edinéia dos Santos Brizola Brum](https://github.com/edibrum)  
- [Jefferson Rodrigo Speck](https://github.com/jeffersonspeck)  
- [Rafael Ferreira Lima](ferreira.rfl@gmail.com)

**Proponente da atividade**: Prof. [Sidgley Camargo de Andrade](https://github.com/sidgleyandrade)
