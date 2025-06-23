# Ciclo Funcional do Sistema

## Fluxo Principal (Execução sem Erros)

1. **Início**
   A aplicação é iniciada a partir do script **`main.py`**.

2. **Configuração de Logs**
   O módulo **`services/logging.py`** configura o sistema de logging com saída para arquivo (e opcionalmente para console), com níveis ajustáveis e criação automática do diretório de logs.

3. **Inicialização do Crawler**
   Para cada URL, um objeto **`PokemonCrawler`** é instanciado.

4. **Descoberta da Página Inicial**

   * A função `discover_pages()` acessa a página inicial (`lista01.htm`) utilizando `requests.get`.
   * Ela extrai todos os links válidos para páginas individuais ou em bloco, elimina duplicatas e retorna a lista ordenada.

5. **Coleta e Análise das Páginas**
   Para cada URL descoberta:

   1. Um novo **`PokemonCrawler(url)`** chama **`fetch_html()`** para obter o HTML.
   2. O conteúdo é processado internamente em **`_parse_tables()`**, usando **BeautifulSoup**.
   3. Cada tabela é transformada por um **`PokemonBuilder`** em um objeto **`Pokemon`**.
   4. Os objetos válidos são adicionados à lista de resultados.

6. **Análise e Exportação**

   * (Opcional) O **`PokemonCSVAnalyzer`** verifica integridade, valores ausentes, tipos de dados e estatísticas.
   * A lista final é exportada para um arquivo CSV via **`write_pokemon_csv()`**, na pasta `output/`.

7. **Encerramento Normal**
   A execução termina normalmente e uma mensagem de sucesso é registrada no log.

---

## Fluxo Alternativo (Tratamento de Erros)

| Etapa                    | Possível Erro                                         | Tratamento                                                                                |
| ------------------------ | ----------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **`fetch_html()`**       | `URLError`, `HTTPError` (falha na conexão)            | O erro é registrado com rastreio e contexto da URL; a próxima URL é tentada               |
| **`_parse_tables()`**    | Tabela malformada ou inconsistências no HTML          | A exceção é capturada e registrada; a tabela é ignorada                                   |
| **Criação de `Pokemon`** | Falta de campos obrigatórios (`number`, `name`)       | O `PokemonBuilder` lança `ValueError`; o erro é registrado e o objeto descartado          |
| **Exportação CSV**       | Falha na escrita (ex.: permissão negada, disco cheio) | A exceção é capturada e registrada; `write_pokemon_csv()` retorna 0 e a execução continua |

> **Nota:** Em todos os casos de erro, o logger registra o **stack trace**, a URL ou tabela afetada e o nível apropriado (`WARNING` ou `ERROR`), facilitando a depuração.
