from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Konfigurasi koneksi MySQL
def get_db_connection():
    koneksi = mysql.connector.connect(
        host='localhost',
        database='crud_db',
        user='root',
        password='HAikak3001'
    )
    return koneksi

@app.route('/')
def index():
    koneksi = get_db_connection()
    cursor = koneksi.cursor(dictionary=True)
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    cursor.close()
    koneksi.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        koneksi = get_db_connection()
        cursor = koneksi.cursor()
        cursor.execute('INSERT INTO items (name, description) VALUES (%s, %s)', (name, description))
        koneksi.commit()
        cursor.close()
        koneksi.close()
        return redirect('/')

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    koneksi = get_db_connection()
    cursor = koneksi.cursor(dictionary=True)
    cursor.execute('SELECT * FROM items WHERE id = %s', (id,))
    item = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        cursor.execute('UPDATE items SET name = %s, description = %s WHERE id = %s', (name, description, id))
        koneksi.commit()
        cursor.close()
        koneksi.close()
        return redirect('/')

    cursor.close()
    koneksi.close()
    return render_template('edit.html', item=item)

@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    koneksi = get_db_connection()
    cursor = koneksi.cursor()
    cursor.execute('DELETE FROM items WHERE id = %s', (id,))
    koneksi.commit()
    cursor.close()
    koneksi.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
