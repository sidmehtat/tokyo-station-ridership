# Tokyo Station Ridership Analysis

Has Shinjuku recovered from the pandemic, and how does it compare with the rest of Tokyo's 10 busiest stations? This project answers that with Japan's official station passenger counts (2011 to 2024), using Python, SQL and PostgreSQL.

> **Status: work in progress.** The file in `data/sample/` holds made-up example numbers that show the data's shape. The real results will replace it as each phase is finished.

## Phases

| Phase | What it does | Status |
|---|---|---|
| 1. Get the data | Download MLIT dataset S12 (station passenger counts) and read its field codes | Done |
| 2. Clean it | Reshape to one row per station, operator and year; keep Tokyo only; drop duplicate-coded rows | In progress |
| 3. Build the database | PostgreSQL tables `stations`, `operators`, `ridership`, loaded from CSV | Not started |
| 4. Write the SQL | Total each station per year, rank by 2019, recovery = 2024 / 2019 x 100 | Not started |
| 5. Make the charts | Bar chart of recovery for the top 10; Shinjuku line chart 2011 to 2024 | Not started |
| 6. Write it up | Findings in this README | Not started |

## Data notes

- Source: [MLIT National Land Numerical Information, S12](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-S12-2024.html).
- Each year has a duplicate code. Only rows coded 1 ("recorded at this line's station") are counted, so riders shared between lines aren't counted twice.
- Station names are Japanese in the source; charts use English names.

## How to run

```bash
python3 -m venv .venv
.venv/bin/pip install pandas matplotlib psycopg2-binary
```

More steps will be added as each phase is finished.
