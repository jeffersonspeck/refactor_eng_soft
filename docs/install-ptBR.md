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
git clone https://github.com/jeffersonspeck/refactor_eng_soft.git
cd refactor_eng_soft
````

2. **Crie um ambiente virtual (opcional, mas recomendado)**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt # Linux/macOS/Windows
```

---

4. **Criação da Documentação dos `.py`**

```bash
#execute o código abaixo se você modificar algo no código, para que gere a nova documentação pelo pdoc

#use uma das linhas abaixo para seu ambiente, caso queira evitar warning do pdoc
set PDOC_DISPLAY_ENV_VARS=1 #cmd windows
$env:PDOC_DISPLAY_ENV_VARS = "1" #powershell
export PDOC_DISPLAY_ENV_VARS=1 #linux

#igual para todos os ambientes
pdoc main.py models services -o docs
```

```bash
#se a documentação já existir ou após você gerar, basta virtualizar o servidor ou acessar os htmls contidos em docs/
python -m http.server --bind 127.0.0.1 --directory docs
```

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
├── docs/                  # documentação
├── output/                # CSVs gerados
├── logs/                  # arquivos de log
├── models/                # definição das entidades
├── services/              # lógica de negócio (crawler, logger, etc.)
└── requirements.txt       # dependências do projeto
```