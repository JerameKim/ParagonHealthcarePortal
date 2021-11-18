from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
#from db_connector import connect_to_database, execute_query
import os

# Configuration
 
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_coughlis'
app.config['MYSQL_PASSWORD'] = '8340'
app.config['MYSQL_DB'] = 'cs340_coughlis'
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

def insert_sample_data():
    cur = mysql.connection.cursor()

    #Insert Addresses
    cur.execute('INSERT INTO Addresses (streetAddress, city, state, zipCode) VALUES ("123 Party Street","Cool Town", "WA", "54321")')
    cur.execute('INSERT INTO Addresses (streetAddress, city, state, zipCode) VALUES ("999 Random House Lane","Wherever", "GA", "01010")')
    cur.execute('INSERT INTO Addresses (streetAddress, city, state, zipCode) VALUES ("1 More Court","Beverly Hills", "WI", "44444")')

    # Insert Patients
    cur.execute('INSERT INTO Patients (patientFirst, patientLast, patientDOB, patientDoc) VALUES ("Zachary","Zucchini", "1994-12-12", 1)')
    cur.execute('INSERT INTO Patients (patientFirst, patientLast, patientDOB, patientDoc) VALUES ("Andrew","Armadillo", "1983-05-03", 1)')
    cur.execute('INSERT INTO Patients (patientFirst, patientLast, patientDOB, patientDoc) VALUES ("Sally","Ride", "1951-05-26", 2)')

    # Insert Procedures

    # Insert Departments

    # Insert Doctors

    # Insert Doctors_Procedures

    # Insert Appointments

# Routes 
@app.route('/')
def root():
    # Connect to database
    cur = mysql.connection.cursor()
    
    # Get a list of commands to run to create tables
    creationCommands = make_commands('./sql_queries/table_creation_queries.sql')
    
    # Disable foreign key checks temporarily, because foreign key collisions are not important when dropping all entities
    cur.execute("SET FOREIGN_KEY_CHECKS=0")
    
    for table in table_names:
        drop_query = "DROP TABLE IF EXISTS %s" % table
        cur.execute(drop_query)
    
    # Re-enable foreign key checks after dropping all tables
    cur.execute("SET FOREIGN_KEY_CHECKS=1")

    for command in creationCommands:
        cur.execute(command)
    
    mysql.connection.commit()

    return render_template('home.html')

# @app.route('/doctors', methods=['PUT', 'POST', 'DELETE'])
@app.route('/doctors')
def doctors():
    return render_template('doctors.html')

# @app.route('/patients', methods=['PUT', 'POST', 'DELETE'])
@app.route('/patients')
def patients():
    return render_template('patients.html')

# @app.route('/procedures', methods=['PUT', 'POST', 'DELETE'])
@app.route('/procedures')
def procedures():
    return render_template('procedures.html')

# @app.route('/departments', methods=['PUT', 'POST', 'DELETE'])
@app.route('/departments')
def departments():
    return render_template('departments.html')

# @app.route('/appointments', methods=['PUT', 'POST', 'DELETE'])
@app.route('/appointments')
def appointments():
    return render_template('appointments.html')

@app.route('/addresses', methods=['GET','PUT', 'POST', 'DELETE'])
#@app.route('/addresses')
def addresses():
    cur = mysql.connection.cursor()

    if request.method == 'PUT':
        pass
    
    cur.execute('SELECT * FROM Addresses')
    result = cur.fetchall()
    mysql.connection.commit()
    print(result)
    return render_template('addresses.html', rows=result)

# @app.route('/doctors-procedures', methods=['PUT', 'POST', 'DELETE'])
@app.route('/doctors-procedures')
def doctors_procedures():
    return render_template('doctors_procedures.html')

# Listener

if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 55557))
    app.run(port=12345, debug= True)
    #app.run(host="flip1.engr.oregonstate.edu", port=51515, debug=False) 
