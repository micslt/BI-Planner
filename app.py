from flask import Flask, render_template, request
import csv
import biplanner

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/fragen1")
def fragen1():
    return render_template("questions1.html")

@app.route("/submit", methods=["POST"])
def submit_form():
    # Die Antworten aus dem Formular abrufen
    analytics_answer1 = request.form.get("analytics_answer1")
    analytics_answer2 = request.form.get("analytics_answer2")
    governance_answer1 = request.form.get("governance_answer1")
    governance_answer2 = request.form.get("governance_answer2")
    # Weitere Antworten für andere Fragen abrufen

    # Eine Liste mit den Antworten erstellen
    answers = [
        analytics_answer1,
        analytics_answer2,
        governance_answer1,
        governance_answer2,
        # Weitere Antworten für andere Fragen hinzufügen
    ]

    # CSV-Datei öffnen und Antworten schreiben
    filename = "antworten.csv"
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(answers)

    # Eine Bestätigungsseite oder eine Weiterleitung anzeigen
    return "Vielen Dank für Ihre Antworten!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
