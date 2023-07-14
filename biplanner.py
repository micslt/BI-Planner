import csv
import os

import csv
import os

def calculate_points_and_save_to_csv(csv_file):
    # Überprüfen, ob die CSV-Datei vorhanden ist
    csv_exists = os.path.isfile(csv_file)

    # Die Punkte berechnen
    organisation = []
    ressourcen = []
    dateninfrastruktur = []
    analytik = []
    governance = []
    with open("reifegrad.csv", "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Header-Zeile überspringen
        for row in reader:
            organisation.append(sum([1 if answer == "ja" else 0 for answer in row[0:6]]))
            ressourcen.append(sum([1 if answer == "ja" else 0 for answer in [row[6]] + row[8:12]]))
            dateninfrastruktur.append(sum([1 if answer == "ja" else 0 for answer in row[13:19]]))
            analytik.append(sum([1 if answer == "ja" else 0 for answer in row[13:19]]))
            governance.append(sum([1 if answer == "ja" else 0 for answer in row[13:19]]))

    # Die Punkte in die CSV-Datei schreiben
    with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Key", "Organisation", "Ressourcen", "Dateninfrastruktur", "Analytik", "Governance" ])
        with open("reifegrad.csv", "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Header-Zeile überspringen
            for row, points1, points2, points3, points4, points5 in zip(reader, organisation, ressourcen, dateninfrastruktur, analytik, governance):
                writer.writerow([row[0], points1, points2, points3, points4, points5])


def get_latest_entry():
    with open("reifegrad_auswertung.csv", "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Header-Zeile überspringen
        latest_entry = max(reader, key=lambda row: row[0])
    return latest_entry[0]

def get_all_entries():
    with open("reifegrad_auswertung.csv", "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Header-Zeile überspringen
        entries = [row[0] for row in reader]
    return entries
