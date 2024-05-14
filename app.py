import yfinance as yf
from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='templates', static_folder='static') 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/transactions')
def transactions():
    return render_template('transactions.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

