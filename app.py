from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('snippets.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                language TEXT NOT NULL,
                code TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect('snippets.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM snippets")
        snippets = cursor.fetchall()
    return render_template('index.html', snippets=snippets)

@app.route('/add', methods=['POST'])
def add_snippet():
    title = request.form['title']
    language = request.form['language']
    code = request.form['code']
    with sqlite3.connect('snippets.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO snippets (title, language, code) VALUES (?, ?, ?)", (title, language, code))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
