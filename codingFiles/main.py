"""
Tokyo Station Ridership Analysis
Siddharth Mehta, 2026

Has Shinjuku recovered from the pandemic, and how does it compare with
Tokyo's other busiest stations? Uses MLIT dataset S12 (2011-2024).

Run from the project folder: python3 codingFiles/main.py
"""

import sys
sys.dont_write_bytecode = True

import datetime

import calculations
import clean

MENU_OPTIONS = [
    "What were Tokyo's 10 busiest stations before the pandemic?",
    "Has Shinjuku recovered from the pandemic?",
    "Which busy stations have recovered the most and the least?",
    "How hard did the pandemic hit each busy station?",
    "How has Shinjuku changed year by year?",
    "Which counts were left out, and why?",
]


def print_welcome():
    print("=" * 50)
    print("       Tokyo Station Ridership Explorer")
    print("=" * 50)
    print("Today:", datetime.date.today().strftime("%B %d, %Y"))
    print("Data:  Japan MLIT dataset S12, station passenger counts")
    print()


def print_menu():
    print()
    print("What do you want to know?")
    number = 1
    for option in MENU_OPTIONS:
        print("  " + str(number) + ". " + option)
        number = number + 1
    print("  0. Quit")


def is_valid_choice(choice):
    if not choice.isdigit():
        return False
    number = int(choice)
    return number >= 0 and number <= len(MENU_OPTIONS)


def get_choice():
    choice = input("Pick a number: ").strip()
    while not is_valid_choice(choice):
        print("'" + choice + "' is not an option. Please pick a number from 0 to " + str(len(MENU_OPTIONS)) + ".")
        choice = input("Pick a number: ").strip()
    return int(choice)


def answer(choice):
    print()
    if choice == 1:
        show_busiest()
    elif choice == 2:
        show_shinjuku_recovery()
    elif choice == 3:
        show_recovery_ranking()
    elif choice == 4:
        show_pandemic_change()
    elif choice == 5:
        show_shinjuku_by_year()
    elif choice == 6:
        show_left_out()


def find_station(name):
    for station_id in calculations.STATION_NAMES:
        if calculations.STATION_NAMES[station_id] == name and station_id in calculations.STATION_TOTALS:
            return station_id
    return None


def show_busiest():
    print("Tokyo's", calculations.TOP_N, "busiest stations in", calculations.BASE_YEAR,
          "(average passengers a day):")
    rank = 1
    for station_id in calculations.TOP_STATIONS:
        name = calculations.STATION_NAMES[station_id]
        total = calculations.STATION_TOTALS[station_id][calculations.BASE_YEAR]
        print("  " + str(rank) + ". " + name + ": " + format(total, ","))
        rank = rank + 1


def show_shinjuku_recovery():
    station_id = find_station("Shinjuku")
    percent = round(calculations.RECOVERY[station_id], 1)
    rank = calculations.RECOVERY_RANKING.index(station_id) + 1

    if percent >= 100:
        print("Yes.", end=" ")
    else:
        print("Not yet.", end=" ")
    print("In", calculations.LATEST_YEAR, "Shinjuku was at " + str(percent) + "% of its",
          calculations.BASE_YEAR, "ridership.")
    print("That ranks", rank, "of", len(calculations.RECOVERY_RANKING),
          "among Tokyo's busiest stations for recovery.")


def show_recovery_ranking():
    print("Recovery of the top", calculations.TOP_N,
          "(" + str(calculations.LATEST_YEAR) + " as a % of " + str(calculations.BASE_YEAR) + "):")
    rank = 1
    for station_id in calculations.RECOVERY_RANKING:
        name = calculations.STATION_NAMES[station_id]
        line = "  " + str(rank) + ". " + name + ": " + str(round(calculations.RECOVERY[station_id], 1)) + "%"
        if name == "Shinjuku":
            line = line + "  <- Shinjuku"
        print(line)
        rank = rank + 1

    most = calculations.RECOVERY_RANKING[0]
    least = calculations.RECOVERY_RANKING[-1]
    print()
    print("Most recovered:", calculations.STATION_NAMES[most] + ".",
          "Least recovered:", calculations.STATION_NAMES[least] + ".")


def show_pandemic_change():
    print("Change from", calculations.BASE_YEAR, "to", calculations.COVID_YEAR, "(the first pandemic year):")
    hardest = None
    for station_id in calculations.PANDEMIC_CHANGE:
        change = calculations.PANDEMIC_CHANGE[station_id]
        print("  " + calculations.STATION_NAMES[station_id] + ": " + str(round(change, 1)) + "%")
        if hardest is None or change < calculations.PANDEMIC_CHANGE[hardest]:
            hardest = station_id
    print()
    print("Hit hardest:", calculations.STATION_NAMES[hardest] + ".")


def show_shinjuku_by_year():
    counts = calculations.CONSISTENT_TOTALS[find_station("Shinjuku")]
    print("Shinjuku, average passengers a day (lines with comparable counts):")
    for year in sorted(counts):
        print("  " + str(year) + ": " + format(counts[year], ","))


def show_left_out():
    print("Lines left out of the recovery figures for the top stations:")
    for key in sorted(calculations.FLAGGED):
        station_id, operator, line = key
        if station_id in calculations.TOP_STATIONS:
            print("  " + calculations.STATION_NAMES[station_id] + ", " + operator + " " + line + ": "
                  + calculations.FLAGGED[key])
    print()
    print("A sudden jump like this means the company changed how it counts, not that riders changed.")


def main():
    print_welcome()

    if not clean.main():
        return

    calculations.run_all()

    choice = -1
    while choice != 0:
        print_menu()
        choice = get_choice()
        if choice != 0:
            answer(choice)
    print("Bye!")


main()
