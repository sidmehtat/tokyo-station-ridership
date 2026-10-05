# calculations.py - reads cleanedData/tokyo_ridership.txt and does all the calculations

import os

PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(PROJECT_FOLDER, "cleanedData", "tokyo_ridership.txt")

BASE_YEAR = 2019
LATEST_YEAR = 2024
COVID_YEAR = 2020
COVID_YEARS = [2020, 2021, 2022]
MAX_JUMP = 0.30
TOP_N = 10

ENGLISH_NAMES = {
    "新宿": "Shinjuku", "渋谷": "Shibuya", "池袋": "Ikebukuro", "東京": "Tokyo",
    "北千住": "Kita-Senju", "品川": "Shinagawa", "新橋": "Shimbashi",
    "高田馬場": "Takadanobaba", "秋葉原": "Akihabara", "上野": "Ueno",
}

ROWS = []
STATION_NAMES = {}
LINES = {}              # (station_id, operator, line) -> {year: passengers}
FLAGGED = {}            # (station_id, operator, line) -> reason
STATION_TOTALS = {}     # station_id -> {year: passengers}
CONSISTENT_TOTALS = {}  # same, but without flagged lines
TOP_STATIONS = []
RECOVERY = {}
RECOVERY_RANKING = []
PANDEMIC_CHANGE = {}


def percent_of(part, whole):
    return part / whole * 100


def percent_change(before, after):
    return (after - before) / before * 100


def add_to(totals, key, year, amount):
    if key not in totals:
        totals[key] = {}
    if year not in totals[key]:
        totals[key][year] = 0
    totals[key][year] = totals[key][year] + amount


def load_rows():
    global ROWS
    ROWS = []
    file = open(DATA_FILE, "r", encoding="utf-8")
    file.readline()
    for line in file:
        parts = line.strip().split(",")
        row = {
            "station_id": parts[0],
            "station": parts[1],
            "operator": parts[2],
            "line": parts[3],
            "year": int(parts[4]),
            "passengers": int(parts[5]),
        }
        ROWS.append(row)
    file.close()


def name_stations():
    global STATION_NAMES
    STATION_NAMES = {}
    for row in ROWS:
        name = row["station"]
        if name in ENGLISH_NAMES:
            name = ENGLISH_NAMES[name]
        STATION_NAMES[row["station_id"]] = name


def group_by_line():
    global LINES
    LINES = {}
    for row in ROWS:
        key = (row["station_id"], row["operator"], row["line"])
        add_to(LINES, key, row["year"], row["passengers"])


def missing_years(counts):
    if BASE_YEAR not in counts or LATEST_YEAR not in counts:
        return "no count for " + str(BASE_YEAR) + " or " + str(LATEST_YEAR)
    return None


def repeats_last_year(counts):
    previous = LATEST_YEAR - 1
    if previous in counts and counts[LATEST_YEAR] == counts[previous]:
        return str(LATEST_YEAR) + " repeats the " + str(previous) + " count"
    return None


def yearly_changes(counts):
    changes = []
    for year in range(BASE_YEAR - 1, LATEST_YEAR):
        next_year = year + 1
        if year in COVID_YEARS or next_year in COVID_YEARS:
            continue
        if year in counts and next_year in counts:
            change = counts[next_year] / counts[year] - 1
            changes.append([year, next_year, change])
    return changes


def sudden_jump(counts):
    # a jump this big outside covid means the company changed how it counts
    for change in yearly_changes(counts):
        year, next_year, amount = change
        if abs(amount) > MAX_JUMP:
            sign = "+" if amount > 0 else "-"
            percent = round(abs(amount) * 100)
            return "jumps " + sign + str(percent) + "% from " + str(year) + " to " + str(next_year)
    return None


def flag_lines():
    global FLAGGED
    FLAGGED = {}
    for key in LINES:
        counts = LINES[key]
        reason = missing_years(counts)
        if reason is None:
            reason = repeats_last_year(counts)
        if reason is None:
            reason = sudden_jump(counts)
        if reason is not None:
            FLAGGED[key] = reason


def total_by_station():
    global STATION_TOTALS, CONSISTENT_TOTALS
    STATION_TOTALS = {}
    CONSISTENT_TOTALS = {}
    for key in LINES:
        station_id = key[0]
        counts = LINES[key]
        for year in counts:
            add_to(STATION_TOTALS, station_id, year, counts[year])
            if key not in FLAGGED:
                add_to(CONSISTENT_TOTALS, station_id, year, counts[year])


def base_year_total(station_id):
    return STATION_TOTALS[station_id][BASE_YEAR]


def find_top_stations():
    global TOP_STATIONS
    stations = []
    for station_id in STATION_TOTALS:
        if BASE_YEAR in STATION_TOTALS[station_id]:
            stations.append(station_id)
    stations.sort(key=base_year_total, reverse=True)
    TOP_STATIONS = stations[:TOP_N]


def calculate_recovery():
    global RECOVERY
    RECOVERY = {}
    for station_id in TOP_STATIONS:
        if station_id not in CONSISTENT_TOTALS:
            continue
        counts = CONSISTENT_TOTALS[station_id]
        if BASE_YEAR in counts and LATEST_YEAR in counts:
            RECOVERY[station_id] = percent_of(counts[LATEST_YEAR], counts[BASE_YEAR])


def recovery_of(station_id):
    return RECOVERY[station_id]


def rank_recovery():
    global RECOVERY_RANKING
    RECOVERY_RANKING = []
    for station_id in RECOVERY:
        RECOVERY_RANKING.append(station_id)
    RECOVERY_RANKING.sort(key=recovery_of, reverse=True)


def calculate_pandemic_change():
    global PANDEMIC_CHANGE
    PANDEMIC_CHANGE = {}
    for station_id in TOP_STATIONS:
        if station_id not in CONSISTENT_TOTALS:
            continue
        counts = CONSISTENT_TOTALS[station_id]
        if BASE_YEAR in counts and COVID_YEAR in counts:
            PANDEMIC_CHANGE[station_id] = percent_change(counts[BASE_YEAR], counts[COVID_YEAR])


def run_all():
    load_rows()
    name_stations()
    group_by_line()
    flag_lines()
    total_by_station()
    find_top_stations()
    calculate_recovery()
    rank_recovery()
    calculate_pandemic_change()
