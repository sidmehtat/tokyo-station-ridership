# Tokyo Station Ridership Analysis

Siddharth Mehta

## Aim

To find out whether Shinjuku Station has recovered from the COVID-19 pandemic, and how its recovery compares with the rest of Tokyo's 10 busiest stations.

## Data source

All data comes from the Japanese government's open data service:

- **Dataset:** National Land Numerical Information, Station Passenger Counts (国土数値情報 駅別乗降客数データ), dataset code S12
- **Publisher:** Ministry of Land, Infrastructure, Transport and Tourism (MLIT), Japan
- **Link:** https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-S12-2024.html
- **File used:** `S12-25_NumberOfPassengers.geojson`, from the download `S12-25_GML.zip`, stored in `rawData/`
- **Contents:** average daily passengers for every station in Japan, fiscal years 2011 to 2024, as reported by each rail company

Credit: 「国土数値情報（駅別乗降客数データ）」（国土交通省）を加工して作成 (created by processing MLIT's Station Passenger Counts data).

`cleanedData/ridership_sample.txt` contains made-up numbers, used only to plan the calculations. No results come from it.

## Method

1. **Clean** (`codingFiles/clean.py`): keep only stations inside a box around central Tokyo, remove counts the dataset marks as duplicates (riders already counted under another line) or as missing, and save the rest to `cleanedData/tokyo_ridership.txt`.
2. **Calculate** (`codingFiles/calculations.py`):
   - add up every rail line at each station for each year
   - rank stations by their 2019 total and keep the top 10
   - recovery = 2024 passengers ÷ 2019 passengers × 100
   - pandemic drop = change from 2019 to 2020
   - leave out of the recovery figures any line whose count jumps more than 30% in a single year outside the pandemic years (2020 to 2022), repeats the previous year's count, or is missing 2019 or 2024, since these point to a change in how the company counts riders
3. **Display** (`codingFiles/main.py`): a numbered menu where the user picks a question and the answer is printed.
