# Manual de Instalação e Uso

Este projeto realiza o **web scraping** de páginas do site [pokemythology.net](https://pokemythology.net), coletando informações de Pokémon e exportando para um arquivo `.csv`. O sistema utiliza `BeautifulSoup`, `requests`, `pandas` e é modularizado com boas práticas de Engenharia de Software.

---

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes)

---

## Instalação

1. **Clone o repositório**

```bash
git clone https://github.com/seu-usuario/pokemon-crawler.git
cd pokemon-crawler
````

2. **Crie um ambiente virtual (opcional, mas recomendado)**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

---

## Configuração

1. Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
START_PAGE=https://pokemythology.net/conteudo/pokemon/lista01.htm
OUTPUT_FILE=output/pokemons.csv
```

2. (Opcional) Certifique-se de que a pasta `output/` existe. Ela será criada automaticamente se necessário.

---

## Execução

Para rodar o projeto, use:

```bash
python main.py
```

O programa irá:

* Ler a URL de início do `.env`
* Descobrir as páginas adicionais de Pokémon
* Extrair dados estruturados
* Gerar um arquivo `pokemons.csv` com os resultados
* Salvar logs em `logs/app.log`
* Exibir no terminal quantos Pokémon foram coletados por página

---

## Estrutura do Projeto

```text
.
├── main.py                # ponto de entrada
├── .env                   # configurações do usuário
├── output/                # CSVs gerados
├── logs/                  # arquivos de log
├── models/                # definição das entidades
├── services/              # lógica de negócio (crawler, logger, etc.)
└── requirements.txt       # dependências do projeto
```

---

## Análise dos Dados

O sistema inclui um analisador de CSV (`PokemonCSVAnalyzer`) que pode, ao final da execução:

* Contar quantos Pokémon foram capturados
* Identificar colunas com valores ausentes
* Verificar duplicações

Os resultados são exibidos no console e/ou registrados no log.

---
