# System Functional Cycle

## Main Flow (Error-Free Execution)

1.  **Start**
   The application starts with the **`main.py`** script.

2.  **Logging Configuration**
   The **`services/logging.py`** module configures logs (file, format, levels).

3.  **Crawler Initialization**
   A **`PokemonCrawler`** class object is instantiated.

4.  **Initial Page Access**
   * The crawler calls **`fetch_html(url)`** to retrieve the `lista01.htm` page.
   * The returned HTML is cleaned and converted into a **`BeautifulSoup`** object (*soup*).

5.  **Secondary Link Discovery**
   The **`discover_pages()`** function collects all links to individual Pokémon or block pages.

6.  **Page Parsing**
   For each discovered URL:
   1.  **`fetch_html`** is called again.
   2.  The content is analyzed in **`_parse_tables`**.
   3.  Each table is transformed into a **`PokemonBuilder`**, then into a **`Pokemon`** object.
   4.  The **`Pokemon`** object is added to the internal list of valid results.

7.  **Analysis and Export**
   * (Optional) **`PokemonCSVAnalyzer`** verifies integrity (nulls, duplicates, statistics).
   * The final list is exported to **`pokemons.csv`** within the `output/` folder.

8.  **Normal Termination**
   The program finishes and logs a success message.

---

## Alternative Flow (Errors)

| Step | Possible Error | Handling |
|---|---|---|
| **`fetch_html`** | `URLError`, `HTTPError` (connection failure) | Error logged with context; crawler continues with the next URL |
| **Parsing (`_parse_tables`)** | Malformed table or missing image | Exception caught and logged; table discarded, loop continues |
| **`Pokemon` Creation** | Essential field missing | `PokemonBuilder` generates a warning in the log and may discard or create an incomplete object |
| **CSV Export** | Write error (permission, file open) | Error logged; application aborts with `exit(1)` or proceeds in degraded mode |

> **Note:** In all error cases, the logger records the **stack trace**, affected URL/table, and appropriate level (`WARNING` or `ERROR`), allowing for quick diagnosis.