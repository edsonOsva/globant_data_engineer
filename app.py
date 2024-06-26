"""
This is a configuration script of a SQLAlchemy DB
"""
from datetime import datetime
from flask import Flask, jsonify, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from sqlalchemy import text
from sqlalchemy.sql import case, func
from random import choice
import pandas as pd
import os

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

#Connecting to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///globant.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
migrate = Migrate(app, db)

#Obtaining json format for records
def to_dict(record):
    dictionary = {}
    for column in record.__table__.columns:
        dictionary[column.name] = getattr(record, column.name)
    return dictionary

#Setting tables within the database:
class Departments(db.Model):
    department_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    department_name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)


class Jobs(db.Model):
    job_id: Mapped[int] = mapped_column(primary_key=True)
    job_name: Mapped[str] = mapped_column(nullable=False)


class Hired(db.Model):
    hired_id: Mapped[int] = mapped_column(primary_key=True)
    hired_name: Mapped[str] = mapped_column(nullable=False)
    hired_date: Mapped[str] = mapped_column(nullable=False)
    hired_department: Mapped[int] = mapped_column(nullable=False)
    hired_job: Mapped[int] = mapped_column(nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload-csv-jobs", methods=["POST"])
def upload_csv_jobs():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    # Guardar el archivo
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # Procesar el archivo CSV
    df = pd.read_csv(file_path, header=None)
    for i in range(len(df)):
        row = df.iloc[i]
        new_row_jobs = Jobs(
            job_id = int(row[0]),
            job_name = str(row[1])
        )
        db.session.add(new_row_jobs)
        db.session.commit()

    return jsonify({"message": f"File {file.filename} successfully uploaded"}), 201

@app.route("/upload-csv-departments", methods=["POST"])
def upload_csv_departments():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    # Guardar el archivo
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # Procesar el archivo CSV
    df = pd.read_csv(file_path, header=None)
    for i in range(len(df)):
        row = df.iloc[i]
        new_row_departments = Departments(
            department_id = int(row[0]),
            department_name = str(row[1])
        )
        db.session.add(new_row_departments)
    db.session.commit()

    return jsonify({"message": f"File {file.filename} successfully uploaded"}), 201


@app.route("/upload-csv-hired", methods=["POST"])
def upload_csv_hired():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    # Guardar el archivo
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # Procesar el archivo CSV
    df = pd.read_csv(file_path, header=None)
    df = df.fillna({1: "No Name", 2: datetime.now(), 3: 0, 4: 0})
    for i in range(len(df)):
        row = df.iloc[i]
        new_row_hired = Hired(
            hired_id = int(row[0]),
            hired_name = str(row[1]),
            hired_date = str(row[2]),
            hired_department = int(row[3]),
            hired_job = int(row[4])
        )
        db.session.add(new_row_hired)
    db.session.commit()

    return jsonify({"message": f"File {file.filename} successfully uploaded"}), 201


@app.route('/hired', methods=['GET'])
def hired_employees():
    query = text("""
        SELECT
            d.department_name,
            j.job_name,
            SUM(CASE WHEN strftime('%m', e.hired_date) BETWEEN '01' AND '03' THEN 1 ELSE 0 END) AS Q1,
            SUM(CASE WHEN strftime('%m', e.hired_date) BETWEEN '04' AND '06' THEN 1 ELSE 0 END) AS Q2,
            SUM(CASE WHEN strftime('%m', e.hired_date) BETWEEN '07' AND '09' THEN 1 ELSE 0 END) AS Q3,
            SUM(CASE WHEN strftime('%m', e.hired_date) BETWEEN '10' AND '12' THEN 1 ELSE 0 END) AS Q4
        FROM
            hired e
        JOIN
            jobs j ON e.hired_job = j.job_id
        JOIN
            departments d ON e.hired_department = d.department_id
        WHERE
            strftime('%Y', e.hired_date) = '2021'
        GROUP BY
            d.department_name,
            j.job_name
        ORDER BY
            d.department_name,
            j.job_name;
        """)

    result = db.session.execute(query).fetchall()

    # Formatear los resultados como una lista de diccionarios
    data = []
    for row in result:
        data.append({
            'department_name': row[0],
            'job_name': row[1],
            'quarter_1': row[2],
            'quarter_2': row[3],
            'quarter_3': row[4],
            'quarter_4': row[5],
        })

    return jsonify(data)


@app.route("/hired-employees-by-department", methods=["GET"])
def hired_employees_by_department():
    query = text(
        """
        SELECT
            d.department_id,
            d.department_name,
            count(h.hired_id) as hired_count
        FROM 
            hired h
        JOIN
            jobs j ON h.hired_job = j.job_id
        JOIN 
            departments d ON h.hired_department = d.department_id
        WHERE 
            strftime('%Y', h.hired_date) = '2021'
        GROUP BY
            d.department_name
        ORDER BY
            hired_count
        DESC"""
    )

    result = db.session.execute(query).fetchall()

    # Formatear los resultados como una lista de diccionarios
    data = []
    for row in result:
        data.append({
            'id': row[0],
            'department': row[1],
            'hired': row[2]
        })

    return jsonify(data)



if __name__ == "__main__":
    app.run(debug=True)