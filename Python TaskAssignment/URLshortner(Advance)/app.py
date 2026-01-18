from flask import Flask, render_template, request, redirect
from models import db, URL, User
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user
)
from werkzeug.security import generate_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
from urllib.parse import urlparse
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = "secret-key-change-later"  # Use environment variable in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def is_valid_url(url):
    parsed = urlparse(url)
    if not (parsed.scheme and parsed.netloc):
        return False
    if '.' not in parsed.netloc:
        return False
    return True

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    short_url = None
    error = None

    if request.method == 'POST':
        original_url = request.form.get('url')

        if not original_url:
            error = "Please enter a URL"

        else:
            if not original_url.startswith(('http://', 'https://')):
                original_url = 'https://' + original_url

                if not is_valid_url(original_url):
                    error = "Please enter a valid URL (example: google.com)"

                else:
                    while True:
                        short_code = generate_short_code()
                        if not URL.query.filter_by(short_code=short_code).first():
                            break
                        
                    short_code = generate_short_code()
                    new_url = URL(
                        original_url=original_url,
                        short_code=short_code,
                        user_id=current_user.id
                        )
                    db.session.add(new_url)
                    db.session.commit()

                    short_url = request.host_url + short_code

    return render_template('home.html', short_url=short_url, error=error)

@app.route('/<short_code>')
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first_or_404()
    return redirect(url.original_url)

@app.route('/history')
@login_required
def history():
    urls = URL.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', urls=urls)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()

        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect('/')
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists"

        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect('/')

    return render_template('signup.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
