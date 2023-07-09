from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')


@app.route("/rahmenbedingungen")
def rahmenbedingungen():
    return render_template("rahmenbedingungen.html")


#############################################################################
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
#######################################################################################

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


#######################################################################################


@app.route("/datenquellen")
def datenquellen():
    return render_template("datenquellen.html")

@app.route("/datenmanagementkonzept")
def datenmanagementkonzept():
    return render_template("datenmanagementkonzept.html")

@app.route("/etl")
def etl():
    return render_template("etl.html")

@app.route("/analysen")
def analysen():
    return render_template("analysen.html")

@app.route("/visualisierung")
def visualisierung():
    return render_template("visualisierung.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/auswertungen")
def auswertungen():
    return render_template("auswertungen.html")

@app.route('/delete_all', methods=['POST'])
def delete_all():
    open('ziele.csv', 'w').close()
    open('reifegrad.csv', 'w').close()
    open('informationsbedarf.csv', 'w').close()
    return redirect('/')
##########################################################################################

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



##############################################################################################

if __name__ == '__main__':
    app.run(debug=True, port=5000)
