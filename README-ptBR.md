# Relatório Técnico de Refatoração

*Projeto Pokémon Crawler – Comparativo entre Código Original e Versão Refatorada*

---

## Documentações auxiliares

1. [Manual de Configuração e Instalação](docs/install.md)
2. [Documentação Técnica](docs/documentation.md)
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

## 1. Links indicados pelo professor

*(preencher posteriormente com as URLs reais)*

| Descrição            | URL |
| -------------------- | --- |
| Leitura indicada     | [Livro](https://engsoftmoderna.info/cap9.html) |
| Página usada em aula | [URL](https://refactoring.guru/pt-br/refactoring/smells) |

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
│   ├── csv_analyzer.py
│   ├── logging.py           # configuração central de logs
│   ├── pokemon_crawler.py   # crawler e parser
│   └── quests.py            # utilidades extra (ex.: missões)
├── output/          # artefatos gerados (pokemons.csv)
├── olds/            # arquivos antigos antes da fatoração (originais do Prof. Sidgley)
└── main.py          # ponto de entrada do aplicativo
```

### 2.1 Principais diferenças estruturais

| Aspecto                   | Código Original (`crawler-pokemon.py`) | Código Refatorado                                            | Ganhos                     |
| ------------------------- | -------------------------------------- | ------------------------------------------------------------ | -------------------------- |
| Organização de pastas     | Arquivo único                          | **Camadas models / services / output**                       | Modularidade, manutenção   |
| Modelo de dados           | `dict` genérico                        | `@dataclass Pokemon` (imutável)                              | Tipagem, segurança         |
| Criação de objeto Pokémon | Lógica espalhada                       | **Builder Pattern** (`PokemonBuilder`)                       | Validação, extensibilidade |
| Parsing & Crawling        | Função única e longa (`crawl_page`)    | Classe `PokemonCrawler` com métodos menores                  | SRP¹, testabilidade        |
| Logging                   | `logging.basicConfig` único            | Função `setup_logging()` com handlers e níveis configuráveis | Logs úteis e padronizados  |
| Análise pós-crawl         | Inexistente                            | `PokemonCSVAnalyzer`                                         | Validação, estatísticas    |
| Organização da saída      | CSV na raiz do projeto                 | CSV em `output/`                                             | Separação de artefatos     |
| Tratamento de erros       | `except Exception` genérico            | Exceções específicas + contexto no log                       | Depuração facilitada       |

> ¹ *SRP – Single Responsibility Principle*.

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

| Code Smell (original)             | Solução / Refactoring                                     |
| --------------------------------- | --------------------------------------------------------- |
| **Método Longo**                  | **Extract Method** + **Extract Class** (`PokemonCrawler`) |
| **Código Duplicado**              | `discover_pages`, `fetch_html` centralizam acesso HTTP    |
| **Obsessão por Tipos Primitivos** | **Extract Class** `Pokemon`                               |
| **Variáveis Globais**             | Mantidas apenas as constantes (candidatas a `Enum`)       |
| **Dependência externa visível**   | Configuração de log centralizada (`setup_logging`)        |
| **Nomes confusos**                | Sugerida renomeação de `logging.py` → `log_config.py`     |
| **Falta de verificação de nulos** | Guard-clauses nos pontos críticos de parsing              |

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

### 6.1 Tabela-síntese solicitada (Que identifiquei após refatoração kkkkkk)

| Code Smell                    | Trecho (novo código)               | Refactoring Executado/Proposto                                           | Comentários                      |
| ----------------------------- | ---------------------------------- | ------------------------------------------------------------------------ | -------------------------------- |
| Métodos Longos                | `_parse_tables` (`PokemonCrawler`) | **Extract Method** – quebrar em `_extract_main_image`, `_parse_kv_pairs` | Ainda >120 LOC; dificulta testes |
| Código Duplicado              | Requests + BS4 parsing             | **Extract Class** (`fetch_html`, `discover_pages`)                       | Reduz redundância                |
| Obsessão por Tipos Primitivos | Representação de Pokémon           | **Extract Class** `Pokemon` + Builder                                    | Modelo forte e validado          |
| Falta de verificação de nulos | Busca de `img` em tabelas          | **Guard-Clause** antes de acessar `.img`                                 | Evita `AttributeError`           |
| Nomes ambíguos                | Módulo `logging.py`                | **Rename Module** (sugerido)                                             | Evita conflito com lib padrão    |

---

## 7. Oportunidades de melhoria e próximos passos

| Tema                       | Ação Recomendada                                                                     |
| -------------------------- | ------------------------------------------------------------------------------------ |
| **Refatoração adicional**  | Quebrar `_parse_tables` em sub-métodos menores.                                      |
| **Enums**                  | Converter `HEADER_COLORS`/`VALUE_COLORS` em `Enum` para evitar *string literals*.    |
| **Tipagem**                | Usar `pydantic` para validação de modelos ou `typing.Annotated`.                     |
| **Testes**                 | Implementar suíte `pytest` com cobertura de >80 %.                                   |
| **CI/CD**                  | Adicionar *pre-commit* (black, isort, ruff) e GitHub Actions.                        |
| **Pattern Strategy**       | Permitir crawlers para múltiplas fontes de dados Pokémon.                            |
| **Tratamento de exceções** | Trocar `except Exception` genérico por exceções específicas (`requests.exceptions`). |
| **Internacionalização**    | Parametrizar mensagens para PT/EN se o projeto for aberto.                           |

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
