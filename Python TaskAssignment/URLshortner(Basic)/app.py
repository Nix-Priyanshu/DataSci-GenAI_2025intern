from flask import Flask, render_template, request, redirect
from models import db, URL
import random
import string
from urllib.parse import urlparse
from urllib.parse import urlparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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
                    short_code = generate_short_code()
                    new_url = URL(
                        original_url=original_url,
                        short_code=short_code
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
def history():
    urls = URL.query.all()
    return render_template('history.html', urls=urls)


if __name__ == '__main__':
    app.run(debug=True)
