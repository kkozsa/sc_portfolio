import yfinance as yf
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, jsonify, session

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = b'11223344'

                                                        # Database config

mysql_host = 'localhost'
mysql_user = 'sqluser'
mysql_password = '123456789'
mysql_db = 'sandc_db'

                                                        # Connect to MySQL

mysql_conn = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_db
)

                                                # Routes

@app.route('/')
def index():
    return render_template('index.html')

                                                        # Login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':                    # User submits login form
        email = request.form['email']
        password = request.form['password']

        cursor = mysql_conn.cursor()                # Cursor interacts with DB
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))        # Query
        user = cursor.fetchone()
        cursor.close()

        if user and user[3] == password:  
            session['email'] = email  
            return redirect(url_for('portfolio'))
        else:
            return "Invalid credentials"

    return render_template('login.html')

                                                        # Portfolio

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

                                                        # Transaction

@app.route('/transactions')
def transactions():
    return render_template('transactions.html')

                                                        # Logout

@app.route('/logout')
def logout():
    session.clear()                         # Clear user data
    return redirect(url_for('login'))

                                                        # Register

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':                    # User submits register form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:            # Checking password match
            return "Passwords do not match!"

        cursor = mysql_conn.cursor()                        # Cursor interacts with DB
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))        # Query
        existing_user = cursor.fetchone()                               # Check if user already exists by email

        if existing_user:
            cursor.close()
            return "User with this email already exists!"

        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))    # Query inserts into user table
        mysql_conn.commit()
        cursor.close()

        return redirect(url_for('login'))               # Back to login page   Maybe change to INDEX

    return render_template('register.html')             # Registration for rendered if GET method

from datetime import datetime

                                                        # Profile

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'email' not in session:                          # Check if the user already logged in
        return redirect(url_for('login'))

    email = session['email']                            
    
    if request.method == 'POST':                        # User submits profile form
        full_name = request.form['full_name']
        date_of_birth = request.form['date_of_birth']
        phone_number = request.form['phone_number']
        address = request.form['address']

        cursor = mysql_conn.cursor()                    # Cursor interacts with DB
        cursor.execute("""
            UPDATE users SET full_name = %s, date_of_birth = %s, phone_number = %s, address = %s        
            WHERE email = %s
        """, (full_name, date_of_birth, phone_number, address, email))      # Profile updated in DB if email matches.
        mysql_conn.commit()
        cursor.close()

        return redirect(url_for('profile'))
    
    cursor = mysql_conn.cursor()                    # Get to fetch profile information
    cursor.execute("SELECT full_name, date_of_birth, phone_number, address FROM users WHERE email = %s", (email,))      # Profile fetch from DB if email matches.
    user_details = cursor.fetchone()
    cursor.close()

    if user_details[1]:                                             # Format date_of_birth to YYYY-MM-DD
        date_of_birth = user_details[1].strftime('%Y-%m-%d')        # 
    else:
        date_of_birth = ""                                          # If not exists, set to empty string

    user = {                                                        # Dictionary for user profile information
        'full_name': user_details[0],
        'date_of_birth': date_of_birth,
        'phone_number': user_details[2],
        'address': user_details[3]
    }

    return render_template('profile.html', user=user)


                                                        # Get stock info

@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    ticker = request.json['ticker']                     # Extract the value ticker from json data
    data = yf.Ticker(ticker).history(period='1y')       # Fetches historical stock price using YF for past 1 year.          Change later
    return jsonify({'currentPrice': data.iloc[-1].Close,
                    'openPrice': data.iloc[-1].Open})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

