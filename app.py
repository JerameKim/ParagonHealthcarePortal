from flask import Flask, render_template, request, redirect
from db_connector import connect_to_database, execute_query
import os

# Configuration
 
app = Flask(__name__)

# Variable to store name of all Tables, to facilitate dropping all when starting up.
table_names = ["Addresses", "Procedures","Departments","Doctors", "Patients", "Appointments", "Doctors_Procedures"]

# Function to execute initial table creation queries
def create_tables(sql_file):
    fd = open(sql_file, 'r')
    query_file = fd.read()
    fd.close()

    creationCommands = query_file.split(';')
    print(creationCommands)

# Routes 
@app.route('/')
def root():
    db_connection = connect_to_database()

    for table in table_names:
        drop_query = "DROP TABLE IF EXISTS %s" % table
        execute_query(db_connection, drop_query)

    

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

# @app.route('/addresses', methods=['PUT', 'POST', 'DELETE'])
@app.route('/addresses')
def addresses():
    return render_template('addresses.html')

# @app.route('/doctors-procedures', methods=['PUT', 'POST', 'DELETE'])
@app.route('/doctors-procedures')
def doctors_procedures():
    return render_template('doctors_procedures.html')

# Listener

if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 55557))
    
    app.run(host="flip1.engr.oregonstate.edu", port=51515, debug=False) 
