from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/reifegrad")
def reifegrad():
    return render_template("reifegrad.html")

@app.route("/rahmenbedingungen")
def rahmenbedingungen():
    return render_template("rahmenbedingungen.html")

@app.route("/unternehmensziele")
def unternehmensziele():
    return render_template("unternehmensziele.html")

@app.route("/informationsbedarf")
def informationsbedarf():
    return render_template("informationsbedarf.html")

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


@app.route("/submit", methods=["POST"])
def submit_form():
    # Die Antworten aus dem Formular abrufen
    frage1 = request.form.get("frage1")
    frage2 = request.form.get("frage2")
    frage3 = request.form.get("frage3")
    frage4 = request.form.get("frage4")
    frage5 = request.form.get("frage5")
    frage6 = request.form.get("frage6")

    # Eine Liste mit den Antworten erstellen
    answers = [frage1, frage2, frage3, frage4, frage5, frage6]

    # CSV-Datei öffnen und Antworten schreiben
    filename = "antworten.csv"
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(answers)

    # Nachricht anzeigen und zur Startseite (index) umleiten
    message = "Ihre Antworten wurden erfasst. Sie werden weitergeleitet."
    return render_template("message.html", message=message, redirect_url="/index")

if __name__ == '__main__':
    app.run()
#if __name__ == '__main__':
#    app.run(debug=True, port=5000)"
