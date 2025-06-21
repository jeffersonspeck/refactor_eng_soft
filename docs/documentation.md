# Ciclo Funcional do Sistema

## Fluxo Principal (Execução sem erros)

1. **Início**  
   A aplicação é iniciada pelo script **`main.py`**.

2. **Configuração de Logging**  
   O módulo **`services/logging.py`** configura os logs (arquivo, formato, níveis).

3. **Inicialização do Crawler**  
   Um objeto da classe **`PokemonCrawler`** é instanciado.

4. **Acesso à Página Inicial**  
   - O crawler chama **`fetch_html(url)`** para obter a página `lista01.htm`.  
   - O HTML retornado é limpo e convertido em objeto **`BeautifulSoup`** (*soup*).

5. **Descoberta de Links Secundários**  
   A função **`discover_pages()`** coleta todos os links para páginas de Pokémon individuais ou blocos.

6. **Parsing das Páginas**  
   Para cada URL descoberta:  
   1. Chama-se novamente **`fetch_html`**.  
   2. O conteúdo é analisado em **`_parse_tables`**.  
   3. Cada tabela é transformada em **`PokemonBuilder`**, depois em **`Pokemon`**.  
   4. O objeto **`Pokemon`** é adicionado à lista interna de resultados válidos.

7. **Análise e Exportação**  
   - (Opcional) **`PokemonCSVAnalyzer`** verifica integridade (nulos, duplicados, estatísticas).  
   - A lista final é exportada para **`pokemons.csv`** dentro da pasta `output/`.

8. **Encerramento Normal**  
   O programa finaliza e grava mensagem de sucesso no log.

---

## Fluxo Alternativo (Erros)

| Etapa | Possível Erro | Tratamento |
|-------|---------------|------------|
| **`fetch_html`** | `URLError`, `HTTPError` (falha de conexão) | Erro logado com contexto; crawler continua com a próxima URL |
| **Parsing (`_parse_tables`)** | Tabela malformada ou sem imagem | Exceção capturada e logada; tabela descartada, loop prossegue |
| **Criação do `Pokemon`** | Campo essencial ausente | `PokemonBuilder` gera aviso no log e pode descartar ou criar objeto incompleto |
| **Exportação CSV** | Erro de escrita (permissão, arquivo aberto) | Erro logado; aplicação aborta com `exit(1)` ou segue em modo degradado |

> **Observação:** em todos os casos de erro, o logger registra **stack trace**, URL/tabela afetada e nível apropriado (`WARNING` ou `ERROR`), permitindo diagnóstico rápido.