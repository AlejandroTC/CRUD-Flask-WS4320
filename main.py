# pip install flask
from flask import Flask, render_template, request, redirect, url_for, flash

# pip install flask-mysqldb
# from flask_mysqldb import MySQL
# pip install pymysql
# from flask_sqlalchemy import SQLAlchemy

# pip install pymysql
import pymysql

# pip install "cloud-sql-python-connector[pymsql]"
from google.cloud.sql.connector import Connector

# pip install sqlalchemy
import sqlalchemy

app = Flask(__name__)
# initialize Connector object
connector = Connector()

# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "sd-atc:us-central1:sd-atc",
        "pymysql",
        user="flask",
        password="Uj+-4l=Cqxqh=4U[",
        db="store",
    )
    return conn


# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# MYSQL CONNECTION localhost
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'admin'
# app.config['MYSQL_DB'] = 'store'
# mysql = MySQL(app)
# Configuración de la conexión a la base de datos de Cloud SQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask:Uj+-4l=Cqxqh=4U[@10.16.48.4/store'
# db = SQLAlchemy(app)

# Settings
app.secret_key = "mysecretkey"

# Ruta para mostrar los empleados


@app.route("/")
def Index():
    with pool.connect() as db_conn:
        employees = db_conn.execute(
            sqlalchemy.text("SELECT * from employees")
        ).fetchall()
        db_conn.commit()
    return render_template("index.html", employees=employees)


# CRUD


@app.route("/add", methods=["POST"])
def add_contact():
    insert_stmt = sqlalchemy.text(
        "INSERT INTO employees (nombre, apellido, fecha_nacimiento) VALUES (:nombre, :apellido, :fecha_nacimiento)",
    )
    if request.method == "POST":
        name = request.form["name"]
        lname = request.form["last_name"]
        bdate = request.form["birth_date"]
        print(name)
        print(lname)
        print(bdate)
        with pool.connect() as db_conn:
            db_conn.execute(
                insert_stmt,
                parameters={
                    "nombre": name,
                    "apellido": lname,
                    "fecha_nacimiento": bdate,
                },
            )
            db_conn.commit()
        flash("Employee added successfully")
        return redirect(url_for("Index"))


@app.route("/edit/<id>")
def get_employee(id):
    # cur = mysql.connection.cursor()
    # cur.execute('SELECT * FROM employees WHERE id = %s', (id) )
    # data = cur.fetchall()
    with pool.connect() as db_conn:
        data = db_conn.execute(
            sqlalchemy.text("SELECT * from employees WHERE id = :id"), {"id": id}
        ).fetchall()
        db_conn.commit()
    return render_template("edit.html", employee=data[0])


@app.route("/update/<id>", methods=["POST"])
def update_employee(id):
    update_stmt = sqlalchemy.text(
        "UPDATE employees SET nombre = :nombre, apellido = :apellido, fecha_nacimiento = :fecha_nacimiento WHERE id = :id"
    )
    if request.method == "POST":
        name = request.form["name"]
        lname = request.form["last_name"]
        bdate = request.form["birth_date"]
        # cur = mysql.connection.cursor()
        # cur.execute("UPDATE employees SET nombre = %s, apellido = %s, fecha_nacimiento = %s WHERE id = %s", (nombre, lname, bdate, id))
        # mysql.connection.commit()
        with pool.connect() as db_conn:
            db_conn.execute(
                update_stmt,
                parameters={
                    "nombre": name,
                    "apellido": lname,
                    "fecha_nacimiento": bdate,
                    "id": id,
                },
            )
            db_conn.commit()
        flash("Employee has been edited")
        return redirect(url_for("Index"))


@app.route("/delete/<id>")
def delete_employ(id):
    # cur = mysql.connection.cursor()
    # cur.execute('DELETE FROM employees WHERE id = {0}'.format(id))
    # print('DELETE FFROM employees WHERE id= {0}'.format(id))
    # mysql.connection.commit()
    with pool.connect() as db_conn:
        # Query para la eliminación
        delete_stmt = sqlalchemy.text("DELETE FROM employees WHERE id = :id")
        parameters = {"id": id}
        db_conn.execute(delete_stmt, parameters)
        db_conn.commit()
    flash("Employee removed successfully")
    return redirect(url_for("Index"))


if __name__ == "__main__":
    app.run(port=3000, debug=False)
