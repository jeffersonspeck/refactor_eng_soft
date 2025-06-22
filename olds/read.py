import pandas as pd
from pathlib import Path

# ----- CONFIGURAÇÃO -----
caminho_csv   = Path("pokemons.csv")         # ⇦ seu arquivo de entrada
caminho_excel = caminho_csv.with_suffix(".xlsx")  # cria mesmo nome, extensão .xlsx
sheet_name    = "Pokemons"                   # nome da planilha no Excel

try:
    # 1) Leitura do CSV
    df = pd.read_csv(caminho_csv, encoding="utf-8")   # ajuste o encoding se preciso

    # 2) Exibe as 10 primeiras linhas (opcional)
    print(df.head(10).to_markdown(tablefmt="grid", index=False))

    # 3) Exporta para Excel
    #    • index=False  → não grava a coluna de índice
    #    • engine="openpyxl" porque é o motor recomendado pelo pandas≥1.4
    df.to_excel(caminho_excel,
                sheet_name=sheet_name,
                index=False,
                engine="openpyxl")

    print(f"\n✔ Arquivo Excel gerado em: {caminho_excel.resolve()}")
except FileNotFoundError:
    print("❌ CSV não encontrado. Verifique o caminho.")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
