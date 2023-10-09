from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
#MYSQL CONNECTION
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'store'
mysql = MySQL(app)

#Settings
app.secret_key = 'mysecretkey'


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM employees')
    data = cur.fetchall()
    print(data)
    return render_template('index.html', employees = data)

#CRUD
@app.route('/add', methods=['POST'])
def add_contact():
    if request.method =='POST':
        name = request.form['name']
        lname = request.form['last_name']
        bdate = request.form['birth_date']
        print(name)
        print(lname)
        print(bdate)
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO employees (nombre, apellido, fecha_nacimiento) VALUES (%s, %s, %s)', (name, lname, bdate))
        mysql.connection.commit()
        flash('Employee added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_employee(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM employees WHERE id = %s', (id) )
    data = cur.fetchall()
    return render_template('edit.html', employee = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_employee(id):
    if request.method == 'POST':
        nombre = request.form['name']
        lname = request.form['last_name']
        bdate = request.form['birth_date']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE employees SET nombre = %s, apellido = %s, fecha_nacimiento = %s WHERE id = %s", (nombre, lname, bdate, id))
        mysql.connection.commit()
        flash('Employee has been edited')
        return redirect(url_for('Index'))

@app.route('/delete/<id>')
def delete_employ(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM employees WHERE id = {0}'.format(id))
    print('DELETE FFROM employees WHERE id= {0}'.format(id))
    mysql.connection.commit()
    flash('Employee removed successfully')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port=3000, debug = True)