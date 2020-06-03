from flask import Flask, g, render_template, request, flash, redirect, abort
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'url_shortener.db'
app.config['SECRET_KEY'] = 'secret'

# connect to database
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

# create the database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# open database connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# close database connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def get_url(id, check_author=True):
    print(id)
    db = get_db()
    url = db.execute(
            'SELECT url FROM url_table WHERE id = ?', (id,)
        ).fetchone()[0]
    print(url)
    if url is None:
        abort(404, "url doesn't exist.".format(id))

    return url

@app.route('/url/<id>')
def redirect_to(id):
    url = get_url(id)
    return redirect(url)
    

@app.route('/')
def home():
    return render_template('index.html', new_url="")

@app.route('/new_url', methods=['GET', 'POST'])
def new_url():
    if request.method == 'POST':
        url = request.form['url']
        db = get_db()
        error = None
        if not url:
            error = 'URL is required.'
        elif db.execute(
            'SELECT id FROM url_table WHERE url = ?', (url,)
        ).fetchone() is not None:
            error = 'Url {} is already \
                   registered.'.format(url)

        if error is None:
            db.execute(
                'INSERT INTO url_table (url) VALUES (?)', (url,)
            )
            db.commit()
            # return redirect('index.html')

        flash(error)

        new_url = 'http://localhost:5000/url/' + str(db.execute(
            'SELECT id FROM url_table WHERE url = ?', (url,)
        ).fetchone()[0])
    return render_template('index.html', new_url=new_url)

if __name__ == '__main__':
    app.run(debug=True)