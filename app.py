from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
from flask import request


@app.route('/frage', methods=['GET', 'POST'])
def frage():
    if request.method == 'POST':
        frage = request.form['frage']
        antwort = beantworte_frage(frage)  # Hier kannst du deine Logik zur Beantwortung der Frage implementieren
        return f'Deine Frage: {frage}<br>Antwort: {antwort}'
    return '''
    <form method="post">
        <input type="text" name="frage" placeholder="Stelle eine Frage">
        <input type="submit" value="Frage stellen">
    </form>
    '''

def beantworte_frage(frage):
    # Implementiere hier deine Logik zur Beantwortung der Frage
    return 'Antwort auf deine Frage'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
