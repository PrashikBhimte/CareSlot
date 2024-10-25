import mysql.connector as ms

db = ms.connect(
    host = "localhost",
    user = "root",
    password = "Pra@290603",
    database = "HMS",
    ssl_disabled = True
)

cursor = db.cursor()

query1 = """CREATE TABLE doctors (
    doc_id INT,
    name VARCHAR(50),
    gender CHAR,
    dob DATE,
    phoneNo BIGINT,
    address VARCHAR(250),
    email VARCHAR(50),
    doj DATE,
    qualification VARCHAR(30),
    PRIMARY KEY (doc_id)
    );
"""
cursor.execute(query1)

query2 = """CREATE TABLE employees (
    emp_id INT,
    name VARCHAR(50),
    gender CHAR,
    dob DATE,
    phoneNo BIGINT,
    address VARCHAR(250),
    email VARCHAR(50),
    doj DATE,
    qualification VARCHAR(30),
    designation VARCHAR(30),
    PRIMARY KEY (emp_id)
    );
"""
cursor.execute(query2)

query3 = """CREATE TABLE doctors_login (
    doc_id INT,
    username VARCHAR(30),
    password VARCHAR(15)
    );
"""
cursor.execute(query3)

query4 = """CREATE TABLE emp_login (
    username VARCHAR(30),
    password VARCHAR(15),
    authority CHAR
    );
"""
cursor.execute(query4)

query5 = """CREATE TABLE patient_personal_details (
    id INT,
    name VARCHAR(50),
    gender CHAR,
    dob DATE,
    phoneNo BIGINT,
    address VARCHAR(250),
    email VARCHAR(50),
    PRIMARY KEY (id)
    );
"""
cursor.execute(query5)

query6 = """CREATE TABLE patient_med_details (
    id INT,
    date DATE,
    medication VARCHAR(250),
    advise VARCHAR(250),
    symptoms VARCHAR(250),
    PRIMARY KEY (id)
    );
"""
cursor.execute(query6)

query7 = """CREATE TABLE patient_login (
    id INT,
    username VARCHAR(30),
    password VARCHAR(15)
    );
"""
cursor.execute(query7)

query8 = """CREATE TABLE appointment (
    app_id INT,
    date DATE,
    time_slot CHAR(14), 
    pat_id INT,
    doc_id INT
    );
"""
cursor.execute(query8)
#time-slot formate : "11:15 to 11:30"

db.close()