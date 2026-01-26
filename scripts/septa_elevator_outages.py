import sys
import requests
import polars as pl
from pathlib import Path
from datetime import datetime, timezone

def get_elevator_status(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        data_list = data.get("results")
        meta = data.get("meta")

        if data_list is None or meta is None:
            print("Error: API response missing 'results' and/or 'meta' keys.")
            sys.exit(1)
        
        if not data_list:
            print("Note: API returned 'results', but it is empty (no active outages).")
            return pl.DataFrame()
        
        df = (
            pl.DataFrame(data_list)
                .with_columns([
                    pl.lit(meta.get("updated", "N/A"))
                        .alias("source_updated_time"),
                    pl.lit(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%S%Z"))
                        .alias("extracted_at_utc")
                ])
            )
        return df
    except Exception as e:
        print(f"Critical error fetching SEPTA data: {e}")
        sys.exit(1)

def main():
    URL = "https://www3.septa.org/api/elevator/index.php"
    FOLDER = Path("./data/septa_elevator_outages")
    FILE_PATH = FOLDER / "septa_elevator_outage_history.csv"

    FOLDER.mkdir(parents=True, exist_ok=True)

    new_outages = get_elevator_status(URL)

    if new_outages.is_empty():
        return

    if FILE_PATH.exists():
        history = pl.read_csv(FILE_PATH)
        updated_df = pl.concat([history, new_outages], how="diagonal_relaxed")
    else:
        updated_df = new_outages

    updated_df.write_csv(FILE_PATH)
    print(f"Success: Logged {new_outages.height} outages to {FILE_PATH}")

if __name__ == "__main__":
    main()
