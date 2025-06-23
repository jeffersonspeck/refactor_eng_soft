# System Functional Cycle

## Main Flow (Error-Free Execution)

1. **Start**
   The application starts with the **`main.py`** script.

2. **Logging Configuration**
   The **`services/logging.py`** module configures logging with file and optional console output, customizable levels, and directory handling.

3. **Crawler Initialization**
   For each URL, a **`PokemonCrawler`** object is instantiated.

4. **Initial Page Discovery**

   * The `discover_pages()` function downloads the initial page (`lista01.htm`) using `requests.get`.
   * It extracts all valid Pokémon-related subpages (individual or block pages), filters duplicates, and returns them sorted.

5. **Page Crawling and Parsing**
   For each discovered URL:

   1. A new **`PokemonCrawler(url)`** calls **`fetch_html()`** to retrieve the HTML content.
   2. The content is parsed in **`_parse_tables()`** using **BeautifulSoup**.
   3. Each table is passed to **`PokemonBuilder`**, which creates a validated **`Pokemon`** object.
   4. Valid Pokémon objects are accumulated in the result list.

6. **Analysis and Export**

   * (Optional) The **`PokemonCSVAnalyzer`** runs integrity checks (missing values, types, stats).
   * The result is written to a CSV file using **`write_pokemon_csv()`** in the `output/` folder.

7. **Normal Termination**
   The program completes its execution and logs a success message with a summary.

---

## Alternative Flow (Errors)

| Step                   | Possible Error                                     | Handling                                                                                      |
| ---------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **`fetch_html()`**     | `URLError`, `HTTPError` (connection failure)       | Error is logged with stack trace and URL context; next URL is attempted                       |
| **`_parse_tables()`**  | Malformed HTML structure or table inconsistency    | Exception is caught and logged; that table is skipped                                         |
| **`Pokemon` Creation** | Missing required fields (`number`, `name`)         | `PokemonBuilder` raises `ValueError`; the error is logged, object skipped                     |
| **CSV Export**         | Write failure (e.g., permission denied, disk full) | Exception is caught; error is logged; `write_pokemon_csv()` returns 0 and execution continues |

> **Note:** In all error cases, the logger records the **stack trace**, affected URL or table, and an appropriate log level (`WARNING` or `ERROR`), enabling effective debugging.
