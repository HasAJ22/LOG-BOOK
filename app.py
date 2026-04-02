from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# DATABASE INIT
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logbook (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarikh TEXT,
            kapal TEXT,
            aktiviti TEXT,
            masalah TEXT,
            tahapkeseriusan TEXT,
            tindakan TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# HOME PAGE
@app.route('/')
def home():
    return render_template('home.html')

# VIEW LOGBOOK + DASHBOARD
@app.route('/logbook')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM logbook")
    data = c.fetchall()
    conn.close()

    total = len(data)
    high = sum(1 for d in data if d[5] == 'High')
    medium = sum(1 for d in data if d[5] == 'Medium')
    low = sum(1 for d in data if d[5] == 'Low')

    return render_template('index.html', data=data, total=total, high=high, medium=medium, low=low)

# ADD LOG
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute("""
            INSERT INTO logbook (tarikh, kapal, aktiviti, masalah, tahapkeseriusan, tindakan)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            request.form['tarikh'],
            request.form['kapal'],
            request.form['aktiviti'],
            request.form['masalah'],
            request.form['tahapkeseriusan'],
            request.form['tindakan']
        ))

        conn.commit()
        conn.close()

        return redirect('/logbook')

    return render_template('add.html')

# DELETE
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM logbook WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/logbook')

# EDIT
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    if request.method == 'POST':
        c.execute("""
            UPDATE logbook
            SET tarikh=?, kapal=?, aktiviti=?, masalah=?, severity=?, tindakan=?
            WHERE id=?
        """, (
            request.form['tarikh'],
            request.form['kapal'],
            request.form['aktiviti'],
            request.form['masalah'],
            request.form['tahapkeseriusan'],
            request.form['tindakan'],
            id
        ))

        conn.commit()
        conn.close()
        return redirect('/logbook')

    c.execute("SELECT * FROM logbook WHERE id=?", (id,))
    data = c.fetchone()
    conn.close()

    return render_template('edit.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)