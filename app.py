from flask import Flask, render_template, request, redirect
import csv
import os
import pandas as pd
import biplanner

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/einfuehrung')
def einfuehrung():
    return render_template('einfuehrung.html')

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
    try:
        with open('reifegrad_auswertung.csv', "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Header-Zeile überspringen
            all_entries = biplanner.get_all_entries()
            selected_entry = request.args.get("key", default=biplanner.get_latest_entry())
            results = [row for row in reader if row[0] == selected_entry]
    except FileNotFoundError:
        reifegrad_auswertung.csv =[]

    return render_template("reifegrad_auswertung.html", results=results, all_entries=all_entries, selected_entry=selected_entry)


"""@app.route('/reifegrad_auswertung/delete', methods=['POST'])
def delete_reifegrad_auswertung():
    reifegrad_nummer = request.form['reifegrad_auswertung_nummer']

    # Lesen Sie alle reifegrad_auswertungen
    with open('reifegrad_auswertung.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        reifegrad_auswertung = [row for row in reader]

    # Löschen Sie das ausgewählte Ziel
    del reifegrad_auswertung[int(reifegrad_nummer) - 1]

    # Überschreiben Sie die CSV-Datei mit den verbleibenden reifegrad_auswertungen
    with open('reifegrad_auswertung.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for reifegrad in reifegrad_auswertung:
            writer.writerow([reifegrad])

    return redirect('/reifegrad_auswertung')"""


##############################################2. Rahmenbedingungen######################################################


@app.route('/rahmenbedingungen', methods=['GET', 'POST'])
def rahmenbedingungen():
    if request.method == 'POST':
        betrieb = request.form["betrieb"]
        aufbau = request.form["aufbau"]
        personenressourcen = request.form["personenressourcen"]
        knowhow = request.form["knowhow"]
        bedarf = request.form["bedarf"]
        mittel = request.form["mittel"]
        personendaten = request.form["personendaten"]
        gesetzeslage = request.form["gesetzeslage"]
        gesetz = request.form["gesetz"]

        with open('rahmenbedingungen.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([betrieb, aufbau, personenressourcen, knowhow, bedarf, mittel, personendaten, gesetzeslage, gesetz])

        return redirect('/rahmenbedingungen')  # Zurück zur Startseite umleiten
    else:
        try:
            with open('rahmenbedingungen.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                # enumerate() wird verwendet, um sowohl die Rahmenbedingungen als auch deren Nummern zu bekommen.
                rahmenbedingungen = [(i, row) for i, row in enumerate(reader, start=1)]
        except FileNotFoundError:
            rahmenbedingungen = []

    return render_template('rahmenbedingungen.html', rahmenbedingungen=rahmenbedingungen)


@app.route('/rahmenbedingungen/delete', methods=['POST'])
def delete_rahmenbedingung():
    rahmenbedingung_nummer = request.form['rahmenbedingung_nummer']

    # Lesen Sie alle rahmenbedingungen
    with open('rahmenbedingungen.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        rahmenbedingungen = [row[0] for row in reader]

    # Löschen Sie das ausgewählte Ziel
    del rahmenbedingungen[int(rahmenbedingung_nummer) - 1]

    # Überschreiben Sie die CSV-Datei mit den verbleibenden rahmenbedingungenn
    with open('rahmenbedingungen.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for rahmenbedingung in rahmenbedingungen:
            writer.writerow([rahmenbedingung])

    return redirect('/rahmenbedingungen')




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
    csv_file = "ziele.csv"

    if not os.path.isfile(csv_file):
       return redirect("/nodata")  # Wenn die Datei nicht vorhanden ist, auf "nodata" umleiten

    if request.method == 'POST':
        bezeichnung = request.form['bezeichnung']
        betroffenes_ziel = request.form['betroffenes_ziel']
        prioritaet = request.form.get('prioritaet', '-')  # Standardwert "-" verwenden, falls nicht angegeben

        with open('informationsbedarf.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([bezeichnung, betroffenes_ziel, prioritaet])

        return redirect('/informationsbedarf')
    else:
        try:
            with open('informationsbedarf.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                informationsbedarf_liste = [(i, row) for i, row in enumerate(reader, start=1)]
        except FileNotFoundError:
            informationsbedarf_liste = []

    dropdown_options = biplanner.load_unternehmensziele()

    return render_template('informationsbedarf.html', informationsbedarf_liste=informationsbedarf_liste, dropdown_options=dropdown_options)



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
        anwendung = request.form['datenquelle']
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


@app.route("/datenmanagementkonzept", methods=['GET', 'POST'])
def datenmanagementkonzept():
    if request.method == 'POST':
        konzeption = request.form['konzeption']
        architektur = request.form['architektur']
        applikation = request.form['applikation']

        with open('datenmanagementkonzept.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([konzeption, architektur, applikation])

        return redirect('/datenmanagementkonzept')  # Änderung hier, um zur Startseite zurückzukehren
    else:
        try:
            with open('datenmanagementkonzept.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                # enumerate() wird verwendet, um sowohl die datenmanagementkonzept als auch deren Nummern zu bekommen.
                datenmanagementkonzept = [(i, row) for i, row in enumerate(reader, start=1)]
        except FileNotFoundError:
            datenmanagementkonzept = []

    return render_template('datenmanagementkonzept.html', datenmanagementkonzept=datenmanagementkonzept)


@app.route('/datenmanagementkonzept/delete', methods=['POST'])
def delete_datenmanagementkonzept():
    datenmanagement_nummer = request.form['datenmanagement_nummer']

    # Lesen Sie alle datenmanagementkonzept
    with open('datenmanagementkonzept.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        datenmanagementkonzept = [row for row in reader]

    # Löschen Sie die ausgewählte Datenquelle
    del datenmanagementkonzept[int(datenmanagement_nummer) - 1]

    # Überschreiben Sie die CSV-Datei mit den verbleibenden datenmanagementkonzept
    with open('datenmanagementkonzept.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for datenmanagement in datenmanagementkonzept:
            writer.writerow(datenmanagement)

    return redirect('/datenmanagementkonzept')




@app.route("/etl", methods=["GET", "POST"])
def etl():
    csv_file = "datenquellen.csv"

    if not os.path.isfile(csv_file):
       return redirect("/nodata")  # Wenn die Datei nicht vorhanden ist, auf "nodata" umleiten

    dropdown_options = biplanner.load_datenquellen()

    return render_template("etl.html", dropdown_options=dropdown_options)

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
    return render_template("message.html", message=message, redirect_url="/analysen")
##################################################5. Informationsgenerierung############################################

@app.route("/analysen", methods=['GET', 'POST'])
def analysen():
    csv_file = "informationsbedarf.csv"

    if not os.path.isfile(csv_file):
       return redirect("/nodata")  # Wenn die Datei nicht vorhanden ist, auf "nodata" umleiten

    if request.method == 'POST':
        analyse = request.form['informationsbedarf']
        messzahl = request.form['messzahl']
        berechnung = request.form['berechnung']
        art = request.form['art']

        with open('analysen.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([analyse, messzahl, berechnung, art])

        return redirect('/analysen')  # Änderung hier, um zur Startseite zurückzukehren
    else:
        try:
            with open('analysen.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                # enumerate() wird verwendet, um sowohl die analysen als auch deren Nummern zu bekommen.
                analysen = [(i, row) for i, row in enumerate(reader, start=1)]
        except FileNotFoundError:
            analysen = []

    dropdown_options = biplanner.load_informationsbedarf()

    return render_template('analysen.html', analysen=analysen, dropdown_options=dropdown_options)



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

@app.route("/informationsbereitstellung", methods=['GET', 'POST'])
def informationsbereitstellung():
    csv_file = "informationsbedarf.csv"

    if not os.path.isfile(csv_file):
       return redirect("/nodata")  # Wenn die Datei nicht vorhanden ist, auf "nodata" umleiten

    if request.method == 'POST':
        bezeichnung = request.form['bezeichnung']
        bereitstellungsart = request.form['bereitstellungsart']
        berechtigte_empfaenger = request.form['berechtigte_empfaenger']
        messung1 = request.form.getlist('messung1[]')

        with open('informationsbereitstellung.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([bezeichnung, bereitstellungsart, berechtigte_empfaenger, messung1])

        return redirect('/informationsbereitstellung')  # Änderung hier, um zur Startseite zurückzukehren
    else:
        try:
            with open('informationsbereitstellung.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                # enumerate() wird verwendet, um sowohl die informationsbereitstellung als auch deren Nummern zu bekommen.
                informationsbereitstellung = [(i, row) for i, row in enumerate(reader, start=1)]
        except FileNotFoundError:
            informationsbereitstellung = []

    dropdown_options = biplanner.load_analysen()


    return render_template('informationsbereitstellung.html', informationsbereitstellung=informationsbereitstellung, dropdown_options=dropdown_options)


@app.route('/informationsbereitstellung/delete', methods=['POST'])
def delete_information():
    information_nummer = request.form['information_nummer']

    # Lesen Sie alle informationsbereitstellung
    with open('informationsbereitstellung.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        informationsbereitstellung = [row for row in reader]

    # Löschen Sie die ausgewählte information
    del informationsbereitstellung[int(information_nummer) - 1]

    # Überschreiben Sie die CSV-Datei mit den verbleibenden informationsbereitstellung
    with open('informationsbereitstellung.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for information in informationsbereitstellung:
            writer.writerow(information)

    return redirect('/informationsbereitstellung')


""""@app.route("/visualisierung")
def visualisierung():
    dropdown_options = biplanner.load_analysen()

    return render_template("visualisierung.html", dropdown_options=dropdown_options)


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
    return render_template("message.html", message=message, redirect_url="/visualisierung")
"""

@app.route("/visualisierung", methods=['GET', 'POST'])
def visualisierung():
    if request.method == 'POST':
        Visualisierung = request.form['Visualisierung']
        qualitaet = request.form['summe']

        with open('visualisierung.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([Visualisierung, qualitaet])

        return redirect('/visualisierung')  # Änderung hier, um zur Startseite zurückzukehren
    else:
        try:
            with open('visualisierung.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                # enumerate() wird verwendet, um sowohl die visualisierung als auch deren Nummern zu bekommen.
                visualisierung = [(i, row) for i, row in enumerate(reader, start=1)]
        except FileNotFoundError:
            visualisierung = []

    dropdown_options = biplanner.load_analysen()

    return render_template('visualisierung.html', visualisierung=visualisierung, dropdown_options=dropdown_options)


@app.route('/visualisierung/delete', methods=['POST'])
def delete_visual():
    visual_nummer = request.form['visual_nummer']

    # Lesen Sie alle visualisierung
    with open('visualisierung.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        visualisierung = [row for row in reader]

    # Löschen Sie die ausgewählte visual
    del visualisierung[int(visual_nummer) - 1]

    # Überschreiben Sie die CSV-Datei mit den verbleibenden visualisierung
    with open('visualisierung.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for visual in visualisierung:
            writer.writerow(visual)

    return redirect('/visualisierung')




@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        dashboard = request.form['dashboard']
        qualitaet = request.form['summe']

        with open('dashboard.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([dashboard, qualitaet])

        return redirect('/dashboard')  # Änderung hier, um zur Startseite zurückzukehren
    else:
        try:
            with open('dashboard.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                # enumerate() wird verwendet, um sowohl die dashboard als auch deren Nummern zu bekommen.
                dashboard = [(i, row) for i, row in enumerate(reader, start=1)]
        except FileNotFoundError:
            dashboard = []

    dropdown_options = biplanner.load_informationsbereitstellung()

    return render_template('dashboard.html', dashboard=dashboard, dropdown_options=dropdown_options)


@app.route('/dashboard/delete', methods=['POST'])
def delete_dash():
    dash_nummer = request.form['dash_nummer']

    # Lesen Sie alle dashboard
    with open('dashboard.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        dashboard = [row for row in reader]

    # Löschen Sie die ausgewählte dash
    del dashboard[int(dash_nummer) - 1]

    # Überschreiben Sie die CSV-Datei mit den verbleibenden dashboard
    with open('dashboard.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for dash in dashboard:
            writer.writerow(dash)

    return redirect('/dashboard')


##################################################7. Auswertungen#######################################################

@app.route("/auswertungen")
def auswertungen():
    try:
        with open('reifegrad_auswertung.csv', "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Header-Zeile überspringen
            all_entries = biplanner.get_all_entries()
            selected_entry = request.args.get("key", default=biplanner.get_latest_entry())
            results = [row for row in reader if row[0] == selected_entry]
    except FileNotFoundError:
        reifegrad_auswertung.csv =[]

    try:
        with open('ziele.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            # enumerate() wird verwendet, um sowohl die Ziele als auch deren Nummern zu bekommen.
            ziele = [(i, row[0]) for i, row in enumerate(reader, start=1)]
    except FileNotFoundError:
        ziele = []

    try:
        with open('informationsbedarf.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                informationsbedarf_liste = [(i, row) for i, row in enumerate(reader, start=1)]
    except FileNotFoundError:
        informationsbedarf_liste = []

    try:
        with open('datenquellen.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            # enumerate() wird verwendet, um sowohl die Datenquellen als auch deren Nummern zu bekommen.
            datenquellen = [(i, row) for i, row in enumerate(reader, start=1)]
    except FileNotFoundError:
        datenquellen = []

    try:
        with open('analysen.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            # enumerate() wird verwendet, um sowohl die analysen als auch deren Nummern zu bekommen.
            analysen = [(i, row) for i, row in enumerate(reader, start=1)]
    except FileNotFoundError:
        analysen = []


    try:
        with open('datenmanagementkonzept.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            # enumerate() wird verwendet, um sowohl die datenmanagementkonzept als auch deren Nummern zu bekommen.
            datenmanagementkonzept = [(i, row) for i, row in enumerate(reader, start=1)]
    except FileNotFoundError:
        datenmanagementkonzept = []

    try:
        with open('rahmenbedingungen.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            # enumerate() wird verwendet, um sowohl die Rahmenbedingungen als auch deren Nummern zu bekommen.
            rahmenbedingungen = [(i, row) for i, row in enumerate(reader, start=1)]
    except FileNotFoundError:
        rahmenbedingungen = []


    try:
        with open('informationsbereitstellung.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            # enumerate() wird verwendet, um sowohl die informationsbereitstellung als auch deren Nummern zu bekommen.
            informationsbereitstellung = [(i, row) for i, row in enumerate(reader, start=1)]
    except FileNotFoundError:
        informationsbereitstellung = []

    try:
        with open('visualisierung.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            # enumerate() wird verwendet, um sowohl die visualisierung als auch deren Nummern zu bekommen.
            visualisierung = [(i, row) for i, row in enumerate(reader, start=1)]
    except FileNotFoundError:
        visualisierung = []

    try:
        with open('dashboard.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            # enumerate() wird verwendet, um sowohl die visualisierung als auch deren Nummern zu bekommen.
            dashboard = [(i, row) for i, row in enumerate(reader, start=1)]
    except FileNotFoundError:
        dashboard = []

    return render_template("auswertungen.html", results=results, all_entries=all_entries, selected_entry=selected_entry,
                           ziele=ziele, informationsbedarf_liste=informationsbedarf_liste, datenquellen=datenquellen,
                           analysen=analysen, datenmanagementkonzept=datenmanagementkonzept,
                           rahmenbedingungen=rahmenbedingungen, informationsbereitstellung=informationsbereitstellung,
                           visualisierung=visualisierung, dashboard=dashboard)

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

@app.route("/nodata")
def nodata():
    return render_template("nodata.html")



if __name__ == '__main__':
    app.run(debug=True, port=5000)
