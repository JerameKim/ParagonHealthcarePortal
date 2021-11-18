from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
#from db_connector import connect_to_database, execute_query
import os

# Configuration
 
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
# app.config['MYSQL_USER'] = 'cs340_coughlis'
app.config['MYSQL_USER'] = 'cs340_kimjera'
# app.config['MYSQL_PASSWORD'] = '8340'
app.config['MYSQL_PASSWORD'] = '1572'

# app.config['MYSQL_DB'] = 'cs340_coughlis'
app.config['MYSQL_DB'] = 'cs340_kimjera'

app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Variable to store name of all Tables, to facilitate dropping all when starting up.
table_names = ["Addresses", "Procedures","Departments","Doctors", "Patients", "Appointments", "Doctors_Procedures"]

# This function receives a file path as a string, and returns a list containing a command written in the file in each index.
# The function expect the file to have each query on it's own, single line, ending with a ;. There must not be additional new lines between queries.
def make_commands(sql_file):
    fd = open(sql_file, 'r')
    query_file = fd.read()
    fd.close()

    creationCommands = query_file.split(';\n')

    return creationCommands

# Under constructoion: was thinking we could call this to populate sample data in the home route down the road.
def insert_sample_data():
    cur = mysql.connection.cursor()

    # #Insert Addresses
    cur.execute('INSERT INTO Addresses (streetAddress, city, state, zipCode) VALUES ("123 Party Street","Cool Town", "WA", "54321")')
    cur.execute('INSERT INTO Addresses (streetAddress, city, state, zipCode) VALUES ("999 Random House Lane","Wherever", "GA", "01010")')
    cur.execute('INSERT INTO Addresses (streetAddress, city, state, zipCode) VALUES ("1 More Court","Beverly Hills", "WI", "44444")')

    # Insert Patients
    # cur.execute('INSERT INTO Patients (patientFirst, patientLast, patientDOB, patientDoc) VALUES ("Zachary","Zucchini", "1994-12-12", 1)')
    # cur.execute('INSERT INTO Patients (patientFirst, patientLast, patientDOB, patientDoc) VALUES ("Andrew","Armadillo", "1983-05-03", 1)')
    # cur.execute('INSERT INTO Patients (patientFirst, patientLast, patientDOB, patientDoc) VALUES ("Sally","Ride", "1951-05-26", 2)')

    # Insert Procedures
    # cur.execute('INSERT INTO Procedures (prcedureName, inPatient) VALUES ("Eyebrow Removal", 1)')

    # Insert Departments
    cur.execute('INSERT INTO Departments (departmentName, departmentHead, addressID) VALUES ("Bone Department", NULL, 1)')
    cur.execute('INSERT INTO Departments (departmentName, departmentHead, addressID) VALUES ("Main Surgery", NULL, 2)')
    cur.execute('INSERT INTO Departments (departmentName, departmentHead, addressID) VALUES ("Pharmacy", NULL, 2)')


    # Insert Doctors
    # cur.execute('INSERT INTO Doctors (doctorFirst, doctorLast, doctorDOB, departmentID) VALUES ("Dorian", "Grey", "1999-09-09, 1)')

    # Insert Doctors_Procedures
    # cur.execute('INSERT INTO Doctors_Procedures (procedureID, doctorID) VALUES (1, 1)')

    # Insert Appointments
    # cur.execute('INSERT INTO Appointments (patientID, doctorID, procedureID, appointmentDate) VALUES (1, 1, 1, "2000-10-10")')

    mysql.connection.commit()

# Routes 
@app.route('/')
def root():
    # Connect to database
    cur = mysql.connection.cursor()
    
    # Get a list of commands to run to create tables
    creationCommands = make_commands('./sql_queries/table_creation_queries.sql')
    
    # Disable foreign key checks temporarily, because foreign key collisions are not important when dropping all entities
    cur.execute("SET FOREIGN_KEY_CHECKS=0")
    
    # Drop all possible tables
    for table in table_names:
        drop_query = "DROP TABLE IF EXISTS %s" % table
        cur.execute(drop_query)
    
    # Re-enable foreign key checks after dropping all tables
    cur.execute("SET FOREIGN_KEY_CHECKS=1")

    for command in creationCommands:
        cur.execute(command)
    
    mysql.connection.commit()

    insert_sample_data()

    return render_template('home.html')

@app.route('/doctors', methods=['GET', 'PUT', 'POST', 'DELETE'])
def doctors():
    cur = mysql.connection.cursor() 

    cur.execute('SELECT * FROM Doctors') 
    result = cur.fetchall()
    mysql.connection.commit()
    print(result)
    return render_template('doctors.html', rows=result)

@app.route('/patients', methods=['GET', 'PUT', 'POST', 'DELETE'])
def patients():
    cur = mysql.connection.cursor()
    
    cur.execute('SELECT * FROM Patients')
    result = cur.fetchall()
    mysql.connection.commit()
    # print(result)
    return render_template('patients.html', rows=result)

@app.route('/procedures', methods=['GET', 'PUT', 'POST', 'DELETE'])
def procedures():
    cur = mysql.connection.cursor()
    
    cur.execute('SELECT * FROM Procedures')
    result = cur.fetchall()
    mysql.connection.commit()
    # print(result)
    return render_template('procedures.html', rows=result)

@app.route('/departments', methods=['GET', 'PUT', 'POST', 'DELETE'])
def departments():
    cur = mysql.connection.cursor() 

    cur.execute('SELECT * FROM Departments') 
    result = cur.fetchall()
    mysql.connection.commit()
    print(result)
    return render_template('departments.html', rows=result)

@app.route('/appointments', methods=['GET', 'PUT', 'POST', 'DELETE'])
def appointments():
    cur = mysql.connection.cursor()
    
    cur.execute('SELECT * FROM Appointments')
    result = cur.fetchall()
    mysql.connection.commit()
    # print(result)
    return render_template('appointments.html', rows=result)

@app.route('/addresses', methods=['GET','PUT', 'POST', 'DELETE'])
#@app.route('/addresses')
def addresses():
    cur = mysql.connection.cursor()
    
    cur.execute('SELECT * FROM Addresses')
    result = cur.fetchall()
    mysql.connection.commit()
    # print(result)
    return render_template('addresses.html', rows=result)

@app.route('/doctors-procedures', methods=['GET', 'PUT', 'POST', 'DELETE'])
def doctors_procedures():
    cur = mysql.connection.cursor()
    
    cur.execute('SELECT * FROM Doctors_Procedures')
    result = cur.fetchall()
    mysql.connection.commit()
    # print(result)
    return render_template('doctors_procedures.html', rows=result)

# Listener

if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 55557))
    app.run(port=12345, debug= True)
    #app.run(host="flip1.engr.oregonstate.edu", port=51515, debug=False) 
