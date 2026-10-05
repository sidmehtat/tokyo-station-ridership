# clean.py - converts the raw government file into cleanedData/tokyo_ridership.txt

import json
import os

PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_FILE = os.path.join(PROJECT_FOLDER, "rawData", "S12-25_NumberOfPassengers.geojson")
CLEAN_FILE = os.path.join(PROJECT_FOLDER, "cleanedData", "tokyo_ridership.txt")

FIRST_YEAR = 2011
LAST_YEAR = 2024

LAT_MIN = 35.53
LAT_MAX = 35.82
LON_MIN = 139.56
LON_MAX = 139.92


def field_names_for_year(year):
    # each year has 4 fields starting at S12_006: duplicate code, status code, notes, passengers
    number = 6 + (year - FIRST_YEAR) * 4
    duplicate_field = "S12_" + str(number).zfill(3)
    status_field = "S12_" + str(number + 1).zfill(3)
    passengers_field = "S12_" + str(number + 3).zfill(3)
    return duplicate_field, status_field, passengers_field


def load_features():
    file = open(RAW_FILE, "r", encoding="utf-8")
    data = json.load(file)
    file.close()
    return data["features"]


def midpoint(feature):
    coordinates = feature["geometry"]["coordinates"]
    total_lat = 0
    total_lon = 0
    for point in coordinates:
        total_lon = total_lon + point[0]
        total_lat = total_lat + point[1]
    return total_lat / len(coordinates), total_lon / len(coordinates)


def find_tokyo_groups(features):
    lat_totals = {}
    lon_totals = {}
    counts = {}
    for feature in features:
        group_code = feature["properties"]["S12_001g"]
        lat, lon = midpoint(feature)
        if group_code not in counts:
            lat_totals[group_code] = 0
            lon_totals[group_code] = 0
            counts[group_code] = 0
        lat_totals[group_code] = lat_totals[group_code] + lat
        lon_totals[group_code] = lon_totals[group_code] + lon
        counts[group_code] = counts[group_code] + 1

    tokyo_groups = []
    for group_code in counts:
        lat = lat_totals[group_code] / counts[group_code]
        lon = lon_totals[group_code] / counts[group_code]
        if LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX:
            tokyo_groups.append(group_code)
    return tokyo_groups


def collect_rows(features, tokyo_groups):
    rows = []
    duplicates_removed = 0
    empty_removed = 0

    for feature in features:
        p = feature["properties"]
        if p["S12_001g"] not in tokyo_groups:
            continue
        for year in range(FIRST_YEAR, LAST_YEAR + 1):
            duplicate_field, status_field, passengers_field = field_names_for_year(year)
            duplicate = p[duplicate_field]
            status = p[status_field]
            passengers = p[passengers_field]

            # duplicate code 2 = already counted under another line
            if duplicate != 1:
                duplicates_removed = duplicates_removed + 1
            elif status != 1 or passengers is None or passengers == 0:
                empty_removed = empty_removed + 1
            else:
                rows.append([p["S12_001g"], p["S12_001"], p["S12_002"], p["S12_003"], year, passengers])

    return rows, duplicates_removed, empty_removed


def sort_order(row):
    return (row[0], row[2], row[3], row[4])


def write_clean_file(rows):
    file = open(CLEAN_FILE, "w", encoding="utf-8")
    file.write("station_id,station,operator,line,year,passengers\n")
    for row in rows:
        station_id, station, operator, line, year, passengers = row
        file.write(station_id + "," + station + "," + operator + "," + line + ","
                   + str(year) + "," + str(passengers) + "\n")
    file.close()


def main():
    if not os.path.exists(RAW_FILE):
        print("The government data file is missing:", RAW_FILE)
        return False

    features = load_features()
    tokyo_groups = find_tokyo_groups(features)
    rows, duplicates_removed, empty_removed = collect_rows(features, tokyo_groups)
    rows.sort(key=sort_order)
    write_clean_file(rows)

    print("Converted", len(features), "stations in Japan down to", len(rows), "Tokyo counts")
    print("(removed", duplicates_removed, "duplicate counts and", empty_removed, "empty ones)")
    return True
