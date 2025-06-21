# Installation and Usage Manual

This project performs **web scraping** of pages from the [pokemythology.net](https://pokemythology.net) website, collecting Pokémon information and exporting it to a `.csv` file. The system uses `BeautifulSoup`, `requests`, `pandas`, and is modularized with good Software Engineering practices.

-----

## Prerequisites

  - Python 3.8 or higher
  - pip (package manager)

-----

## Installation

1.  **Clone the repository**

    ```bash
    git clone https://github.com/jeffersonspeck/refactor_eng_soft.git
    cd refactor_eng_soft
    ```

2.  **Create a virtual environment (optional, but recommended)**

    ```bash
    python -m venv venv
    source venv/bin/activate    # Linux/macOS
    venv\Scripts\activate       # Windows
    ```

3.  **Install dependencies**

    ```bash
    pip install -r requirements.txt # Linux/macOS/Windows
    ```

-----

4.  **Generating `.py` Documentation**

    ```bash
    #execute the code below if you modify anything in the code, to generate new documentation with pdoc

    #use one of the lines below for your environment if you want to avoid pdoc warnings
    set PDOC_DISPLAY_ENV_VARS=1 #cmd windows
    $env:PDOC_DISPLAY_ENV_VARS = "1" #powershell
    export PDOC_DISPLAY_ENV_VARS=1 #linux

    #same for all environments
    pdoc main.py models services -o docs
    ```

    ```bash
    #if the documentation already exists or after you generate it, just virtualize the server or access the html files in docs/
    python -m http.server --bind 127.0.0.1 --directory docs
    ```

## Configuration

1.  Create a `.env` file in the project root with the following content:

    ```env
    START_PAGE=https://pokemythology.net/conteudo/pokemon/lista01.htm
    OUTPUT_FILE=output/pokemons.csv
    ```

2.  (Optional) Ensure the `output/` folder exists. It will be created automatically if needed.

-----

## Execution

To run the project, use:

```bash
python main.py
```

The program will:

  * Read the starting URL from the `.env` file
  * Discover additional Pokémon pages
  * Extract structured data
  * Generate a `pokemons.csv` file with the results
  * Save logs in `logs/app.log`
  * Display in the terminal how many Pokémon were collected per page

-----

## Project Structure

```text
.
├── main.py                 # entry point
├── .env                    # user configurations
├── docs/                   # documentation
├── output/                 # generated CSVs
├── logs/                   # log files
├── models/                 # entity definitions
├── services/               # business logic (crawler, logger, etc.)
└── requirements.txt        # project dependencies
```