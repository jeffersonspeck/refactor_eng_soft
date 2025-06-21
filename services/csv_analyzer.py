# services/csv_analyzer.py
import logging
import pandas as pd
from collections import defaultdict

class PokemonCSVAnalyzer:
    """Utility class to run different validations/report on a Pokémon CSV."""
    
    def __init__(self, csv_path: str, encoding: str = "utf-8"):
        self.csv_path = csv_path
        self.encoding = encoding
        try:
            self.df = pd.read_csv(csv_path, encoding=encoding)
            logging.info("CSV loaded successfully from '%s' (%d rows, %d columns)",
                         csv_path, len(self.df), len(self.df.columns))
        except Exception:
            logging.error("Failed to load CSV '%s'", csv_path, exc_info=True)
            raise
    
    # -------------------------------------------------
    # Public analysis methods
    # -------------------------------------------------
    
    def log_summary(self) -> None:
        """Logs basic dataset information (rows, cols, dtypes, head, stats)."""
        logging.info("=== Dataset summary ===")
        logging.info("Total rows   : %d", len(self.df))
        logging.info("Total columns: %d", len(self.df.columns))
        logging.info("Column names : %s", list(self.df.columns))

        # dtypes
        logging.info("Column dtypes:")
        for col, dtype in self.df.dtypes.items():
            logging.info("  • %-20s %s", col, dtype)

        # first rows
        logging.info("First 5 rows:")
        for idx, row in self.df.head(5).iterrows():
            logging.info("  Row %d → %s", idx, row.to_dict())

        # stats (numeric + object)
        stats = self.df.describe(include='all').transpose()
        logging.info("Statistical summary:")
        for col in stats.index:
            logging.info("  • %-20s %s", col, stats.loc[col].dropna().to_dict())

    def log_missing_values(self) -> None:
        """Logs number of missing (blank or whitespace) cells per column."""
        missing = self.df.isna() | (self.df.astype(str).apply(lambda col: col.str.strip() == "", axis=0))
        missing_counts = missing.sum()
        total_missing = missing_counts.sum()

        logging.info("=== Missing-value check ===")
        if total_missing == 0:
            logging.info("All columns are fully populated.")
            return

        logging.warning("Found %d missing value(s) across the dataset.", total_missing)
        for col, cnt in missing_counts[missing_counts > 0].sort_values(ascending=False).items():
            logging.warning("  • %-20s %d missing", col, cnt)

    # convenience: run everything at once
    def run_full_report(self) -> None:
        self.log_summary()
        self.log_missing_values()