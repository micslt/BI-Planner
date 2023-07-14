from flask import Flask, render_template, request, redirect
import csv
import os
import pandas as pd
import biplanner

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

###################################1. Standortbestimmung################################################################

@app.route("/reifegrad")
def reifegrad():
    return render_template("reifegrad.html")

import csv
from datetime import datetime

@app.route("/reifegrad_submit", methods=["POST"])
def submit_reifegrad():
    if request.method == "POST":
        form_data = request.form

        # Überprüfe, ob die CSV-Datei vorhanden ist
        csv_exists = os.path.isfile("reifegrad.csv")

        with open("reifegrad.csv", "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            # Schreibe Header, falls CSV-Datei neu erstellt wurde
            if not csv_exists:
                header = list(form_data.keys())
                header.insert(0, "eingabe")
                writer.writerow(header)

            # Aktuelles Datum und Uhrzeit hinzufügen
            now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            form_data_values = list(form_data.values())
            form_data_values.insert(0, now)

            writer.writerow(form_data_values)

        biplanner.calculate_points_and_save_to_csv("reifegrad_auswertung.csv")

        # Nachricht anzeigen und zur Startseite (index) umleiten
        message = "Ihre Antworten wurden erfasst. Sie werden weitergeleitet."
        return render_template("message.html", message=message, redirect_url="/reifegrad_auswertung")



@app.route("/reifegrad_auswertung")
def reifegrad_auswertung():
    all_entries = biplanner.get_all_entries()
    selected_entry = request.args.get("key", default=biplanner.get_latest_entry())

    results = []
    with open("reifegrad_auswertung.csv", "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Header-Zeile überspringen
        for row in reader:
            if row[0] == selected_entry:
                results.append(row)

    return render_template("reifegrad_auswertung.html", results=results, all_entries=all_entries, selected_entry=selected_entry)

##############################################2. Rahmenbedingungen######################################################


@app.route("/rahmenbedingungen", methods=["GET", "POST"])
def rahmenbedingungen():
    return render_template("rahmenbedingungen.html")

@app.route("/submit_rahmenbedingungen", methods=["GET", "POST"])
def submit_rahmenbedingungen():
    if request.method == "POST":
        form_data = request.form

        # Überprüfe, ob die CSV-Datei vorhanden ist
        csv_exists = os.path.isfile("rahmenbedingungen.csv")

        with open("rahmenbedingungen.csv", "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            # Schreibe Header, falls CSV-Datei neu erstellt wurde
            if not csv_exists:
                writer.writerow(form_data.keys())

            writer.writerow(form_data.values())


        # Nachricht anzeigen und zur Startseite (index) umleiten
    message = "Ihre Antworten wurden erfasst. Sie werden weitergeleitet."
    return render_template("message.html", message=message, redirect_url="/rahmenbedingungen")    


##################################################3.Planung#############################################################

@app.route('/unternehmensziele', methods=['GET', 'POST'])
def unternehmensziele():
    if request.method == 'POST':
        ziel = request.form['ziel']
        with open('ziele.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([ziel])
        return redirect('/unternehmensziele')  # Änderung hier, um zur Startseite zurückzukehren
    else:
        try:
            with open('ziele.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                # enumerate() wird verwendet, um sowohl die Ziele als auch deren Nummern zu bekommen.
                ziele = [(i, row[0]) for i, row in enumerate(reader, start=1)]
        except FileNotFoundError:
            ziele = []
    return render_template('unternehmensziele.html', ziele=ziele)

@app.route('/unternehmensziele/delete', methods=['POST'])
def delete_ziel():
    ziel_nummer = request.form['ziel_nummer']

    # Lesen Sie alle Ziele
    with open('ziele.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        ziele = [row[0] for row in reader]

    # Löschen Sie das ausgewählte Ziel
    del ziele[int(ziel_nummer) - 1]

    # Überschreiben Sie die CSV-Datei mit den verbleibenden Zielen
    with open('ziele.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for ziel in ziele:
            writer.writerow([ziel])

    return redirect('/unternehmensziele')


@app.route('/informationsbedarf', methods=['GET', 'POST'])
def informationsbedarf():
    if request.method == 'POST':
        informationsbedarf = request.form['informationsbedarf']
        beschreibung = request.form['beschreibung']
        nutzen = request.form['nutzen']
        typ = request.form['typ']
        metrik = request.form['metrik']
        prioritaet = request.form.get('prioritaet', '-')  # Standardwert "-" verwenden, falls nicht angegeben

        with open('informationsbedarf.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([informationsbedarf, beschreibung, nutzen, typ, metrik, prioritaet])

        return redirect('/informationsbedarf')
    else:
        try:
            with open('informationsbedarf.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                # enumerate() wird verwendet, um sowohl die Informationsbedarfe als auch deren Nummern zu bekommen.
                informationsbedarf_liste = [(i, row) for i, row in enumerate(reader, start=1)]
        except FileNotFoundError:
            informationsbedarf_liste = []
    return render_template('informationsbedarf.html', informationsbedarf_liste=informationsbedarf_liste)


@app.route('/informationsbedarf/delete', methods=['POST'])
def delete_informationsbedarf():
    informationsbedarf_nummer = request.form['informationsbedarf_nummer']

    # Lesen Sie alle Informationsbedarfe
    with open('informationsbedarf.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        informationsbedarf = [row[0] for row in reader]

    # Löschen Sie den ausgewählten Informationsbedarf
    del informationsbedarf[int(informationsbedarf_nummer) - 1]

    # Überschreiben Sie die CSV-Datei mit den verbleibenden Informationsbedarfen
    with open('informationsbedarf.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for informationsbedarf in informationsbedarf:
            writer.writerow([informationsbedarf])

    return redirect('/informationsbedarf')


@app.route("/datenquellen", methods=['GET', 'POST'])
def datenquellen():
    if request.method == 'POST':
        anwendung = request.form['anwendung']
        inhalt = request.form['inhalt']

        with open('datenquellen.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([anwendung, inhalt])

        return redirect('/datenquellen')  # Änderung hier, um zur Startseite zurückzukehren
    else:
        try:
            with open('datenquellen.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                # enumerate() wird verwendet, um sowohl die Datenquellen als auch deren Nummern zu bekommen.
                datenquellen = [(i, row) for i, row in enumerate(reader, start=1)]
        except FileNotFoundError:
            datenquellen = []

    return render_template('datenquellen.html', datenquellen=datenquellen)


@app.route('/datenquellen/delete', methods=['POST'])
def delete_datenquelle():
    datenquelle_nummer = request.form['datenquelle_nummer']

    # Lesen Sie alle Datenquellen
    with open('datenquellen.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        datenquellen = [row for row in reader]

    # Löschen Sie die ausgewählte Datenquelle
    del datenquellen[int(datenquelle_nummer) - 1]

    # Überschreiben Sie die CSV-Datei mit den verbleibenden Datenquellen
    with open('datenquellen.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for datenquelle in datenquellen:
            writer.writerow(datenquelle)

    return redirect('/datenquellen')

##################################################4. Datenbereitstellung################################################


@app.route("/datenmanagementkonzept", methods=["GET", "POST"])
def datenmanagementkonzept():
    return render_template("datenmanagementkonzept.html")

@app.route("/submit_datenmanagementkonzept", methods=["GET", "POST"])
def submit_datenmanagementkonzept():
    if request.method == "POST":
        form_data = request.form

        # Überprüfe, ob die CSV-Datei vorhanden ist
        csv_exists = os.path.isfile("datenmanagementkonzept.csv")

        with open("datenmanagementkonzept.csv", "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            # Schreibe Header, falls CSV-Datei neu erstellt wurde
            if not csv_exists:
                writer.writerow(form_data.keys())

            writer.writerow(form_data.values())


        # Nachricht anzeigen und zur Startseite (index) umleiten
    message = "Ihre Antworten wurden erfasst. Sie werden weitergeleitet."
    return render_template("message.html", message=message, redirect_url="/etl")



@app.route("/etl", methods=["GET", "POST"])
def etl():
    return render_template("etl.html")

@app.route("/submit_etl", methods=["GET", "POST"])
def submit_etl():
    if request.method == "POST":
        form_data = request.form

        # Überprüfe, ob die CSV-Datei vorhanden ist
        csv_exists = os.path.isfile("etl.csv")

        with open("etl.csv", "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            # Schreibe Header, falls CSV-Datei neu erstellt wurde
            if not csv_exists:
                writer.writerow(form_data.keys())

            writer.writerow(form_data.values())


        # Nachricht anzeigen und zur Startseite (index) umleiten
    message = "Ihre Antworten wurden erfasst. Sie werden weitergeleitet."
    return render_template("message.html", message=message, redirect_url="/etl")
##################################################5. Informationsgenerierung############################################

@app.route("/analysen", methods=['GET', 'POST'])
def analysen():
    if request.method == 'POST':
        analyse = request.form['informationsbedarf']
        messzahl = request.form['messzahl']
        art = request.form['art']
        berechnung = request.form['berechnung']

        with open('analysen.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([analyse, messzahl, art, berechnung])

        return redirect('/analysen')  # Änderung hier, um zur Startseite zurückzukehren
    else:
        try:
            with open('analysen.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                # enumerate() wird verwendet, um sowohl die analysen als auch deren Nummern zu bekommen.
                analysen = [(i, row) for i, row in enumerate(reader, start=1)]
        except FileNotFoundError:
            analysen = []

    return render_template('analysen.html', analysen=analysen)


@app.route('/analysen/delete', methods=['POST'])
def delete_analyse():
    analyse_nummer = request.form['analyse_nummer']

    # Lesen Sie alle analysen
    with open('analysen.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        analysen = [row for row in reader]

    # Löschen Sie die ausgewählte analyse
    del analysen[int(analyse_nummer) - 1]

    # Überschreiben Sie die CSV-Datei mit den verbleibenden analysen
    with open('analysen.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for analyse in analysen:
            writer.writerow(analyse)

    return redirect('/analysen')

##################################################6. Informationsbereitstellung#########################################

@app.route("/informationsbereitstellung")
def informationsbereitstellung():
    return render_template("informationsbereitstellung.html")

@app.route("/submit_informationsbereitstellung", methods=["GET", "POST"])
def submit_informationsbereitstellung():
    if request.method == "POST":
        form_data = request.form

        # Überprüfe, ob die CSV-Datei vorhanden ist
        csv_exists = os.path.isfile("informationsbereitstellung.csv")

        with open("informationsbereitstellung.csv", "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            # Schreibe Header, falls CSV-Datei neu erstellt wurde
            if not csv_exists:
                writer.writerow(form_data.keys())

            writer.writerow(form_data.values())

        # Nachricht anzeigen und zur Startseite (index) umleiten
    message = "Ihre Antworten wurden erfasst. Sie werden weitergeleitet."
    return render_template("message.html", message=message, redirect_url="/")

@app.route("/visualisierung")
def visualisierung():
    return render_template("visualisierung.html")

@app.route("/submit_visualisierung", methods=["GET", "POST"])
def submit_visualisierung():
    if request.method == "POST":
        form_data = request.form

        # Überprüfe, ob die CSV-Datei vorhanden ist
        csv_exists = os.path.isfile("visualisierung.csv")

        with open("visualisierung.csv", "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            # Schreibe Header, falls CSV-Datei neu erstellt wurde
            if not csv_exists:
                writer.writerow(form_data.keys())

            writer.writerow(form_data.values())

        # Nachricht anzeigen und zur Startseite (index) umleiten
    message = "Ihre Antworten wurden erfasst. Sie werden weitergeleitet."
    return render_template("message.html", message=message, redirect_url="/")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/submit_dashboard", methods=["GET", "POST"])
def submit_dashboard():
    if request.method == "POST":
        form_data = request.form

        # Überprüfe, ob die CSV-Datei vorhanden ist
        csv_exists = os.path.isfile("dashboard.csv")

        with open("dashboard.csv", "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            # Schreibe Header, falls CSV-Datei neu erstellt wurde
            if not csv_exists:
                writer.writerow(form_data.keys())

            writer.writerow(form_data.values())

        # Nachricht anzeigen und zur Startseite (index) umleiten
    message = "Ihre Antworten wurden erfasst. Sie werden weitergeleitet."
    return render_template("message.html", message=message, redirect_url="/")


##################################################7. Auswertungen#######################################################

@app.route("/auswertungen")
def auswertungen():
    return render_template("auswertungen.html")

##################################################8. Feedback### #######################################################
@app.route("/feedback")
def feedback():
    return render_template("feedback.html")


@app.route("/submit_feedback", methods=["GET", "POST"])
def submit_feedback():
    if request.method == "POST":
        form_data = request.form
        save_feedback(form_data)

    message = "Ihre Antworten wurden erfasst. Sie werden weitergeleitet."
    return render_template("message.html", message=message, redirect_url="/end")

def save_feedback(form_data):
    fieldnames = list(form_data.keys())
    feedback_data = list(form_data.values())

    with open("feedback.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:
            writer.writerow(fieldnames)
        writer.writerow(feedback_data)


@app.route("/feedback_auswertung")
def feedback_auswertung():
    # DataFrame aus CSV erstellen
    df = pd.read_csv("feedback.csv", encoding="utf-8")

    # Daten als HTML-Tabelle rendern
    table_html = df.to_html(index=False)

    return render_template("feedback_auswertung.html", table_html=table_html)

##################################################Functionality#########################################################
@app.route('/delete_all', methods=['POST'])
def delete_all():
    files = ['ziele.csv', 'reifegrad.csv', 'reifegrad_auswertung.csv','informationsbedarf.csv', 'rahmenbedingungen.csv',
             'analysen.csv', 'datenmanagementkonzept.csv', 'datenquellen.csv', 'etl.csv', 'informationsbereitstellung.csv',
             'dashboard.csv', 'visualisierung.csv']

    for file in files:
        if os.path.exists(file):
            os.remove(file)

    return redirect('/deleted')


@app.route("/end")
def end():
    return render_template("end.html")


@app.route("/deleted")
def deleted():
    return render_template("deleted.html")


if __name__ == '__main__':
    app.run(debug=True, port=5000)
