from flask import Flask, render_template, request, redirect, url_for, session
import pyotp
import qrcode
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    totp_secret = db.Column(db.String(16), nullable=True)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    if 'user' in session:
        return render_template('home.html', username=session['user'])
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        totp = pyotp.TOTP(pyotp.random_base32())
        new_user = User(username=username, password=password, totp_secret=totp.secret)
        db.session.add(new_user)
        db.session.commit()
        # Generate QR code
        uri = totp.provisioning_uri(name=username, issuer_name='ExampleApp')
        img = qrcode.make(uri)
        img.save('static/images/qrcode.png')
        return redirect(url_for('setup_2fa'))
    return render_template('register.html')

@app.route('/setup_2fa')
def setup_2fa():
    user = User.query.filter_by(username=session.get('user')).first()
    if not user:
        return redirect(url_for('login'))
    totp = pyotp.TOTP(user.totp_secret)
    uri = totp.provisioning_uri(name=user.username, issuer_name='ExampleApp')
    return render_template('setup_2fa.html', qrcode_uri=uri)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        totp_code = request.form['totp_code']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            totp = pyotp.TOTP(user.totp_secret)
            if totp.verify(totp_code):
                session['user'] = username
                return redirect(url_for('home'))
            else:
                return "Invalid 2FA code"
        else:
            return "Invalid credentials"
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
