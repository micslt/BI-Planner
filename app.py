from flask import Flask, render_template, request, redirect
import csv
import os
import pandas as pd

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

@app.route("/reifegrad_submit", methods=["POST"])
def submit_form():
    # Die Antworten aus dem Formular abrufen
    frage1 = request.form.get("frage1")
    frage2 = request.form.get("frage2")
    frage3 = request.form.get("frage3")
    frage4 = request.form.get("frage4")
    frage5 = request.form.get("frage5")
    frage6 = request.form.get("frage6")
    frage7 = request.form.get("frage7")
    frage8 = request.form.get("frage8")
    frage9 = request.form.get("frage9")
    frage10 = request.form.get("frage10")
    frage11 = request.form.get("frage11")
    frage12 = request.form.get("frage12")
    frage13 = request.form.get("frage13")
    frage14 = request.form.get("frage14")
    frage15 = request.form.get("frage15")
    frage16 = request.form.get("frage16")
    frage17 = request.form.get("frage17")
    frage18 = request.form.get("frage18")
    frage19 = request.form.get("frage19")
    frage20 = request.form.get("frage20")
    frage21 = request.form.get("frage21")
    frage22 = request.form.get("frage22")
    frage23 = request.form.get("frage23")
    frage24 = request.form.get("frage24")
    frage25 = request.form.get("frage25")
    frage26 = request.form.get("frage26")
    frage27 = request.form.get("frage27")
    frage28 = request.form.get("frage28")
    frage29 = request.form.get("frage29")
    frage30 = request.form.get("frage30")
    frage31 = request.form.get("frage31")
    frage32 = request.form.get("frage32")
    frage33 = request.form.get("frage33")
    frage34 = request.form.get("frage34")
    frage35 = request.form.get("frage35")
    frage36 = request.form.get("frage36")

    # Eine Liste mit den Antworten erstellen
    answers = [frage1, frage2, frage3, frage4, frage5, frage6, frage7, frage8, frage9,
               frage10, frage11, frage12, frage13, frage14, frage15, frage16, frage17,
               frage18, frage19, frage20, frage21, frage22, frage23, frage24, frage25,
               frage26, frage27, frage28, frage29, frage30, frage31, frage32, frage33,
               frage34, frage35, frage36]


    # CSV-Datei öffnen und Antworten schreiben
    filename = "reifegrad.csv"
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(answers)

    # Nachricht anzeigen und zur Startseite (index) umleiten
    message = "Ihre Antworten wurden erfasst. Sie werden weitergeleitet."
    return render_template("message.html", message=message, redirect_url="/auswertungen")


##############################################2. Rahmenbedingungen######################################################

@app.route("/rahmenbedingungen", methods=['GET', 'POST'])
def rahmenbedingungen():
    if request.method == 'POST':
        it_betrieben = request.form.get('it_betrieben', '')
        bia_aufbau = request.form.get('bia_aufbau', '')
        personelle_ressourcen = request.form.get('personelle_ressourcen', '')
        knowhow_vorhanden = request.form.get('knowhow_vorhanden', '')
        finanzieller_bedarf = request.form.get('finanzieller_bedarf', '')
        finanzielle_mittel = request.form.get('finanzielle_mittel', '')
        personendaten_analyse = request.form.get('personendaten_analyse', '')
        gesetzeslage = request.form.get('gesetzeslage', '')
        compliance_vorgaben = request.form.getlist('compliance_vorgaben')

        # Speichern der Antworten in einer CSV-Datei
        filename = "rahmenbedingungen.csv"
        with open(filename, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([it_betrieben, bia_aufbau, personelle_ressourcen, knowhow_vorhanden,
                             finanzieller_bedarf, finanzielle_mittel, personendaten_analyse, gesetzeslage,
                             ', '.join(compliance_vorgaben)])

        # Nachricht anzeigen und zur Startseite (index) umleiten
        message = "Ihre Antworten wurden erfasst. Sie werden weitergeleitet."
        return render_template("message.html", message=message, redirect_url="/auswertungen")
    else:
        return render_template("rahmenbedingungen.html")


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

    return render_template("datenmanagementkonzept.html")

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


@app.route("/analysen")
def analysen():
    return render_template("analysen.html")

##################################################6. Informationsbereitstellung#########################################


@app.route("/visualisierung")
def visualisierung():
    return render_template("visualisierung.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

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

@app.route("/end")
def end():
    return render_template("end.html")


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
    open('ziele.csv', 'w').close()
    open('reifegrad.csv', 'w').close()
    open('informationsbedarf.csv', 'w').close()
    open('rahmenbedingungen.csv', 'w').close()
    open('datenmanagementkonzept.csv', 'w').close()
    open('etl.csv', 'w').close()
    return redirect('/')




##############################################################################################

if __name__ == '__main__':
    app.run(debug=True, port=5000)
