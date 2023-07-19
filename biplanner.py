import csv
import os
import pandas as pd

def calculate_points_and_save_to_csv(csv_file):
    # Überprüfen, ob die CSV-Datei vorhanden ist
    csv_exists = os.path.isfile(csv_file)

    # Die Punkte berechnen
    organisation = []
    ressourcen = []
    dateninfrastruktur = []
    analytik = []
    governance = []
    total = []

    comment_organisation = []
    comment_ressourcen = []
    comment_dateninfrastruktur = []
    comment_analytik = []
    comment_governance = []

    with open("reifegrad.csv", "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Header-Zeile überspringen
        for row in reader:
            organisation.append(int(sum([1 if answer == "ja" else 0 for answer in row[1:7]]) / 6 * 100))
            ressourcen.append(int(sum([1 if answer == "ja" else 1 if answer =="5" else 0.75 if answer == "4" else 0.5 if answer == "3" else 0.25 if answer == "2" else 0 for answer in row[7:13]]) / 6 * 100))
            dateninfrastruktur.append(int(sum([1 if answer == "ja" else 0 for answer in row[13:19]])/6*100))
            analytik.append(int(sum([1 if answer == "ja" else 1 if answer == "5" else 0.75 if answer == "4" else 0.5 if answer == "3" else 0.25 if answer == "2" else 0 for answer in row[19:25]])/6*100))
            governance.append(int(sum([1 if answer == "ja" else 0 for answer in row[25:35]])/10*100))
            total.append(int(sum([1 if answer == "ja" else 1 if answer =="5" else 0.75 if answer == "4" else 0.5 if answer == "3" else 0.25 if answer == "2" else 0 for answer in row[1:35]]) / 34 * 100))
            comment_organisation.append("Aus Sicht der Organisation erreicht " if organisation[0]>80 else "kacke")

    # Die Punkte in die CSV-Datei schreiben
    with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Key", "Organisation", "Ressourcen", "Dateninfrastruktur", "Analytik", "Governance", "Total", "Kommentar Organisation" ])
        with open("reifegrad.csv", "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Header-Zeile überspringen
            for row, points1, points2, points3, points4, points5, points6, comment1 in zip(reader, organisation, ressourcen,
                                                                        dateninfrastruktur, analytik, governance, total, comment_organisation):
                writer.writerow([row[0], points1, points2, points3, points4, points5, points6, comment1])


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


def load_unternehmensziele():
    options = []
    with open('ziele.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            options.append(row[0])
    return options

def load_datenquellen():
    options = []
    with open('datenquellen.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            options.append(row[0])
    return options

def load_informationsbedarf():
    options = []
    with open('informationsbedarf.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            options.append(row[0])
    return options

def load_informationsbereitstellung():
    options = []
    with open('informationsbereitstellung.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            options.append(row[0])
    return options

def load_analysen():
    options = []
    with open('analysen.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            options.append(row[1])
    return options

def load_visualisierung():
    summe = 0
    with open('analysen.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            summe += sum(map(int, row[1:13]))
    return summe

def etl_auflistung():
    # Datei einlesen und DataFrame erstellen
    df = pd.read_csv('etl.csv')

    # DataFrame um 90 Grad drehen
    df_transposed = df.transpose()

    return df_transposed

