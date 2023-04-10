from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['guess'] = int(request.form['guess'])
        return redirect(url_for('guess'))
    else:
        session['number'] = random.randint(1, 100)
        return render_template('index.html')

@app.route('/guess', methods=['GET', 'POST'])
def guess():
    if request.method == 'POST':
        session['guess'] = int(request.form['guess'])
    if session['guess'] == session['number']:
        if 'attempts' in session:
            attempts = session['attempts']
        else:
            attempts = 1
        return render_template('win.html', attempts=attempts)
    elif session['guess'] > session['number']:
        message = "Too high"
    else:
        message = "Too low"
    if 'attempts' in session:
        session['attempts'] += 1
    else:
        session['attempts'] = 1
    if session['attempts'] == 10:
        return render_template('lose.html')
    return render_template('guess.html', message=message)

@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    if request.method == 'POST':
        if 'winners' in session:
            winners = session['winners']
        else:
            winners = []
        winners.append({'name': request.form['name'], 'attempts': int(request.form['attempts'])})
        session['winners'] = winners
    return render_template('leaderboard.html', winners=winners)

if __name__ == '__main__':
    app.run(debug=True)
