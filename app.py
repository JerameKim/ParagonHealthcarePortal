from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
# from db_connector import connect_to_database, execute_query
import os

# Configuration
 
app = Flask(__name__)

mysql = MySQL()

# MySQL configurations for Heroku
app.config['MYSQL_USER'] = 'b5144e26b93e3c'
app.config['MYSQL_PASSWORD'] = '2e4abfe4'
app.config['MYSQL_DB'] = 'heroku_5234e1c57267f61'
app.config['MYSQL_HOST'] = 'us-cdbr-east-04.cleardb.com'

# mysql = MySQL(app)
mysql.init_app(app)

app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


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

# Routes 
@app.route('/')
def root():
    # Connect to database
    cur = mysql.connection.cursor()
    
    # Get a list of commands to run to create tables
    creationCommands = make_commands('./sql_queries/table_creation_queries.sql')

    for command in creationCommands:
        cur.execute(command)
    
    mysql.connection.commit()

    # insert_sample_data()

    return render_template('home.html')

@app.route('/doctors', methods=['GET', 'POST', 'DELETE'])
def doctors():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        
        cur.execute('SELECT * FROM Doctors')
        all_doctors = cur.fetchall()

        cur.execute('SELECT * FROM Departments')
        all_departments = cur.fetchall()

        for doctor in all_doctors: 
            if doctor["departmentID"] != None:
                cur.execute(f'SELECT * FROM Departments WHERE departmentID = {doctor["departmentID"]};')
                single_department = cur.fetchall()
                department_name = single_department[0]["departmentName"]
                doctor["departmentID"] = department_name

        mysql.connection.commit()
        return render_template('doctors.html', doctor_list=all_doctors, department_list = all_departments)

    if request.method == "POST": 
        mode = request.form['mode']

        doctorFirst = request.form['doctorFirst']
        doctorLast = request.form['doctorLast']
        doctorDOB = request.form['doctorDOB']
        departmentID = request.form['departmentID']

        cur = mysql.connection.cursor()
        
        if mode=='add':
            cur.execute(f'INSERT INTO Doctors (doctorFirst, doctorLast, doctorDOB, departmentID) VALUES ("{doctorFirst}", "{doctorLast}", "{doctorDOB}", "{departmentID}")')
        
        else:
            doctorID = request.form['doctorID']
            update_query = f'UPDATE Doctors SET doctorFirst="{doctorFirst}", doctorLast="{doctorLast}", doctorDOB="{doctorDOB}", departmentID="{departmentID}" WHERE doctorID={doctorID}'
            cur.execute(update_query)
        
        cur.execute('SELECT * FROM Departments')
        all_departments = cur.fetchall()

        cur.execute('SELECT * FROM Doctors')
        all_doctors = cur.fetchall()

        for doctor in all_doctors: 
            cur.execute(f'SELECT * FROM Departments WHERE departmentID = {doctor["departmentID"]};')
            single_department = cur.fetchall()
            department_name = single_department[0]["departmentName"]
            doctor["departmentID"] = department_name

        mysql.connection.commit()
        return render_template('doctors.html', doctor_list=all_doctors, department_list = all_departments)

@app.route('/patients', methods=['GET', 'POST', 'DELETE'])
def patients():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        
        cur.execute('SELECT * FROM Patients;')
        all_patients = cur.fetchall()

        cur.execute('SELECT * FROM Doctors;')
        all_doctors = cur.fetchall()

        for patient in all_patients: 
            if patient["patientDoc"] != None:

                cur.execute(f'SELECT * FROM Doctors WHERE doctorID = {patient["patientDoc"]};')
                single_doc = cur.fetchall()
                doc_first = single_doc[0]["doctorFirst"]
                doc_last = single_doc[0]["doctorLast"]
                doctor_name = doc_first + " " + doc_last
                patient["patientDoc"] = doctor_name

        mysql.connection.commit()
        return render_template('patients.html', patient_list=all_patients, doctor_list = all_doctors)

    if request.method == "POST": 
        
        mode = request.form['mode']
        
        patientFirst = request.form['patientFirst']
        patientLast = request.form['patientLast']
        patientDOB = request.form['patientDOB']
        doctorID = request.form['doctorID']

        cur = mysql.connection.cursor()
        
        if mode == 'add':
            cur.execute(f'INSERT INTO Patients (patientFirst, patientLast, patientDOB, patientDoc) VALUES ("{patientFirst}", "{patientLast}", "{patientDOB}", "{doctorID}")')
        
        else:
            patientID = request.form['patientID']
            update_query = f'UPDATE Patients SET patientFirst="{patientFirst}", patientLast="{patientLast}", patientDOB="{patientDOB}", patientDoc={doctorID} WHERE patientID={patientID}'
            cur.execute(update_query)

        cur.execute('SELECT * FROM Doctors')
        all_doctors = cur.fetchall()

        cur.execute('SELECT * FROM Patients')
        all_patients = cur.fetchall()
        
        for patient in all_patients: 
            if patient["patientDoc"] != None:
                cur.execute(f'SELECT * FROM Doctors WHERE doctorID = {patient["patientDoc"]};')
                single_doc = cur.fetchall()
                doc_first = single_doc[0]["doctorFirst"]
                doc_last = single_doc[0]["doctorLast"]
                doctor_name = doc_first + " " + doc_last
                # replace patientDoc with string
                patient["patientDoc"] = doctor_name
    
        mysql.connection.commit()
        return render_template('patients.html', patient_list=all_patients, doctor_list = all_doctors)

@app.route('/delete/doctors_procedures/<string:id>')
def delete_doc_proc(id):
    cur = mysql.connection.cursor()

    # Delete using doctor id
    id_list = id.split('+')
    doc_id=id_list[0]
    proc_id=id_list[1]
    cur.execute("SET FOREIGN_KEY_CHECKS=0")
    cur.execute("DELETE FROM Doctors_Procedures WHERE doctorID= %s AND procedureID= %s" % (doc_id, proc_id))    
    cur.execute("SET FOREIGN_KEY_CHECKS=1")

    # Render table
    cur.execute('SELECT * FROM Doctors_Procedures')
    all_doc_procs = cur.fetchall()
    cur.execute('SELECT * FROM Procedures')
    all_procedures = cur.fetchall()
    cur.execute('SELECT * FROM Doctors')
    all_doctors = cur.fetchall()
    mysql.connection.commit()
    return render_template('doctors_procedures.html', doc_proc_list=all_doc_procs, procedure_list = all_procedures, doctor_list = all_doctors)

@app.route('/delete/<string:table>/<int:id>')
def delete(table, id):
    cur = mysql.connection.cursor()
    # Render Patients Table
    if table == "patients": 

        # Do the deleting
        cur.execute("DELETE FROM Patients WHERE patientID = %s" % (id))    

        # Populate table
        cur.execute('SELECT * FROM Doctors')
        all_doctors = cur.fetchall()
        cur.execute('SELECT * FROM Patients')
        all_patients = cur.fetchall()
        
        mysql.connection.commit()
        return render_template('patients.html', patient_list=all_patients, doctor_list = all_doctors)

    # Render Doctors Table
    if table == "doctors": 

        # Do the Deleting
        cur.execute("DELETE FROM Doctors WHERE doctorID = %s" % (id))    

        # Populate table
        cur.execute('SELECT * FROM Doctors')
        result = cur.fetchall()
        cur.execute('SELECT * FROM Departments')
        all_departments = cur.fetchall()
        mysql.connection.commit()
        return render_template('doctors.html', doctor_list=result, department_list = all_departments)

    if table == "procedures":

        cur.execute("DELETE FROM Procedures WHERE procedureID = %s" % (id))    

        # Populate table
        cur.execute('SELECT * FROM Procedures')
        all_procedures = cur.fetchall()
        mysql.connection.commit()
        return render_template('procedures.html', procedure_list=all_procedures)
    
    if table == "departments": 
        # Delete
        cur.execute("DELETE FROM Departments WHERE departmentID= %s" % (id))    

        # Render table
        cur.execute('SELECT * FROM Departments')
        all_departments = cur.fetchall()

        cur.execute('SELECT * FROM Addresses')
        all_addresses = cur.fetchall()

        cur.execute('SELECT * FROM Doctors')
        all_doctors = cur.fetchall()

        mysql.connection.commit()

        return render_template('departments.html', department_list=all_departments, address_list = all_addresses, doctor_list = all_doctors)

    if table == "appointments": 
        # Delete
        cur.execute("DELETE FROM Appointments WHERE appointmentID= %s" % (id))    

        # Render Table
        cur.execute('SELECT * FROM Appointments')
        all_appointments = cur.fetchall()

        cur.execute('SELECT * FROM Patients')
        all_patients = cur.fetchall()

        cur.execute('SELECT * FROM Doctors')
        all_doctors = cur.fetchall()

        cur.execute('SELECT * FROM Procedures')
        all_procedures = cur.fetchall()

        mysql.connection.commit()

        return render_template('appointments.html', appointment_list=all_appointments, patient_list = all_patients, doctor_list = all_doctors, procedure_list=all_procedures)

    if table == "addresses": 
        # Delete
        cur.execute("DELETE FROM Addresses WHERE addressID= %s" % (id))    
        cur = mysql.connection.cursor()
        
        cur.execute('SELECT * FROM Addresses')
        all_addresses = cur.fetchall()
        mysql.connection.commit()
        return render_template('addresses.html', address_list = all_addresses)

@app.route('/procedures', methods=['GET', 'PUT', 'POST', 'DELETE'])
def procedures():
    # Render procedures table
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        
        cur.execute('SELECT * FROM Procedures')
        all_procedures = cur.fetchall()
        mysql.connection.commit()
        return render_template('procedures.html', procedure_list=all_procedures)

    if request.method == "POST": 

        mode = request.form['mode']

        procedureName = request.form['procedureName']
        inPatient = request.form['inPatient']

        cur = mysql.connection.cursor()
        
        if mode == 'add':
            cur.execute(f'INSERT INTO Procedures (procedureName, inPatient) VALUES ("{procedureName}", "{inPatient}")')

        else:
            procedureID = request.form['procedureID']
            update_query = f'UPDATE Procedures SET procedureName="{procedureName}", inPatient="{inPatient}" WHERE procedureID={procedureID}'
            cur.execute(update_query)
        
        cur.execute('SELECT * FROM Procedures')

        all_procedures = cur.fetchall()
        mysql.connection.commit()
        return render_template('procedures.html', procedure_list=all_procedures)

@app.route('/departments', methods=["GET", "POST", "DELETE"])
def departments():

    cur = mysql.connection.cursor()

    if request.method == "GET":
        
        cur.execute('SELECT * FROM Departments')
        all_departments = cur.fetchall()

        cur.execute('SELECT * FROM Addresses')
        all_addresses = cur.fetchall()

        cur.execute('SELECT * FROM Doctors')
        all_doctors = cur.fetchall()

        for department in all_departments: 
            if department["addressID"] != None:
                cur.execute(f'SELECT * FROM Addresses WHERE addressID = {department["addressID"]};')
                single_address = cur.fetchall()
                streetAddress = single_address[0]['streetAddress']
                city = single_address[0]['city']
                state = single_address[0]['state']
                zipCode = single_address[0]['zipCode']
                full_address = streetAddress + ", " + city + ", " + state + " " + zipCode
                department["addressID"] = full_address

            if department["departmentHead"] != None:

                cur.execute(f'SELECT * FROM Doctors WHERE doctorID = {department["departmentHead"]};')
                single_doc = cur.fetchall()
                doc_first = single_doc[0]["doctorFirst"]
                doc_last = single_doc[0]["doctorLast"]
                doctor_name = doc_first + " " + doc_last
                department["departmentHead"] = doctor_name


        mysql.connection.commit()

        return render_template('departments.html', department_list= all_departments, address_list = all_addresses, doctor_list = all_doctors)

    if request.method == "POST":

        mode = request.form['mode']

        if mode == "add":
            departmentName = request.form['departmentName']
            
            departmentHead = request.form['departmentHead']
            departmentAddress = request.form['addressID']
            
            # Check if submitted with no departmentHead, in which case pass NULL with this value.
            if departmentHead != 'NULL':
                cur.execute(f'INSERT INTO Departments (departmentName, departmentHead, addressID) VALUES ("{departmentName}", "{departmentHead}", "{departmentAddress}")')
            else:
                cur.execute(f'INSERT INTO Departments (departmentName, departmentHead, addressID) VALUES ("{departmentName}", NULL, "{departmentAddress}")')
        
        else:
            # get the values from the request

            departmentID = request.form['departmentID']

            if 'departmentName' in request.form:
                departmentName = request.form['departmentName']
            if 'departmentHead' in request.form:
                departmentHead = request.form['departmentHead']
            if 'addressID' in request.form:
                addressID = request.form['addressID']

            # build the query to update
            update_query_not_null = f'UPDATE Departments SET departmentName = "{departmentName}", departmentHead = "{departmentHead}", addressID = "{addressID}" WHERE departmentID = {departmentID}'
            update_query_null = f'UPDATE Departments SET departmentName = "{departmentName}", departmentHead = NULL, addressID = "{addressID}" WHERE departmentID = {departmentID}'

            cur.execute("SET FOREIGN_KEY_CHECKS=0")
            # execute the query
            if departmentHead == 'NULL':
                cur.execute(update_query_null)
            else:
                cur.execute(update_query_not_null)
            cur.execute("SET FOREIGN_KEY_CHECKS=1")

        cur.execute('SELECT * FROM Departments')
        all_departments = cur.fetchall()

        cur.execute('SELECT * FROM Addresses')
        all_addresses = cur.fetchall()

        cur.execute('SELECT * FROM Doctors')
        all_doctors = cur.fetchall()
        
        for department in all_departments: 
            if department["addressID"] != None:
                cur.execute(f'SELECT * FROM Addresses WHERE addressID = {department["addressID"]};')
                single_address = cur.fetchall()
                streetAddress = single_address[0]['streetAddress']
                city = single_address[0]['city']
                state = single_address[0]['state']
                zipCode = single_address[0]['zipCode']
                full_address = streetAddress + ", " + city + ", " + state + " " + zipCode
                department["addressID"] = full_address

            if department["departmentHead"] != None:

                cur.execute(f'SELECT * FROM Doctors WHERE doctorID = {department["departmentHead"]};')
                single_doc = cur.fetchall()
                doc_first = single_doc[0]["doctorFirst"]
                doc_last = single_doc[0]["doctorLast"]
                doctor_name = doc_first + " " + doc_last
                department["departmentHead"] = doctor_name

        mysql.connection.commit()
        return render_template('departments.html', department_list=all_departments, address_list = all_addresses, doctor_list = all_doctors)

@app.route('/<string:table>/update', methods=['POST'])
def update_entity(table):
    # Set cursor
    cur = mysql.connection.cursor()

    if table == "departments":
        # Get id for the chosen row
        this_deptID = request.form['departmentID']

        # Get data for the chosen row
        query = f'SELECT * FROM Departments WHERE departmentID={this_deptID}'
        cur.execute(query)
        this_dept = cur.fetchone()

        cur.execute('SELECT * FROM Addresses')
        all_addresses = cur.fetchall()

        cur.execute('SELECT * FROM Doctors')
        all_doctors = cur.fetchall()

        cur.execute('SELECT * FROM Departments')
        all_departments = cur.fetchall()

        for department in all_departments: 
            if department["addressID"] != None:
                cur.execute(f'SELECT * FROM Addresses WHERE addressID = {department["addressID"]};')
                single_address = cur.fetchall()
                streetAddress = single_address[0]['streetAddress']
                city = single_address[0]['city']
                state = single_address[0]['state']
                zipCode = single_address[0]['zipCode']
                full_address = streetAddress + ", " + city + ", " + state + " " + zipCode
                department["addressID"] = full_address

        # Pass to the new template to be rendered
        return render_template('update_dept.html', department = this_dept, address_list = all_addresses, doctor_list = all_doctors)

    if table == "addresses":
        # Get id for the chosen row
        this_addrID = request.form['addressID']

        # Get data for the chosen row
        query = f'SELECT * FROM Addresses WHERE addressID={this_addrID}'
        cur.execute(query)
        this_addr = cur.fetchone()

        # Pass to the new template to be rendered
        return render_template('update_addresses.html', address = this_addr)

    if table == 'patients':
        # Get id for the chosen row
        this_patientID = request.form['patientID']

        # Get data for the chosen row
        query = f'SELECT * FROM Patients WHERE patientID={this_patientID}'
        cur.execute(query)
        this_patient = cur.fetchone()

        cur.execute("SELECT * FROM Doctors")
        all_doctors = cur.fetchall()
        
        cur.execute("SELECT * FROM Patients") 
        all_patients = cur.fetchall()

        for patient in all_patients: 
            if patient["patientDoc"] != None:
                cur.execute(f'SELECT * FROM Doctors WHERE doctorID = {patient["patientDoc"]};')
                single_doc = cur.fetchall()
                doc_first = single_doc[0]["doctorFirst"]
                doc_last = single_doc[0]["doctorLast"]
                doctor_name = doc_first + " " + doc_last
                patient["patientDoc"] = doctor_name

        # Pass to the new template to be rendered
        return render_template('update_patients.html', patient = this_patient, doctor_list=all_doctors)

    if table == 'doctors':
        # Get id for the chosen row
        this_doctorID = request.form['doctorID']

        # Get data for the chosen row
        query = f'SELECT * FROM Doctors WHERE doctorID={this_doctorID}'
        cur.execute(query)
        this_doctor = cur.fetchone()

        cur.execute('SELECT * FROM Departments')
        all_departments = cur.fetchall()

        cur.execute('SELECT * FROM Doctors')
        all_doctors = cur.fetchall()

        for doctor in all_doctors: 
            if doctor["departmentID"] != None:
                cur.execute(f'SELECT * FROM Departments WHERE departmentID = {doctor["departmentID"]};')
                single_department = cur.fetchall()
                department_name = single_department[0]["departmentName"]
                # replace patientDoc with string
                doctor["departmentID"] = department_name

        # Pass to the new template to be rendered
        return render_template('update_doctors.html', doctor = this_doctor, department_list = all_departments)

    if table == 'appointments':
        # Get id for the chosen row
        this_apptID = request.form['appointmentID']

        # Get data for the chosen row
        query = f'SELECT * FROM Appointments WHERE appointmentID={this_apptID}'
        cur.execute(query)
        this_appt = cur.fetchone()

        cur.execute("SELECT * FROM Patients")
        all_patients = cur.fetchall()

        cur.execute("SELECT * FROM Doctors")
        all_doctors = cur.fetchall()

        cur.execute("SELECT * FROM Procedures")
        all_procedures = cur.fetchall()

        cur.execute("SELECT * FROM Appointments")
        all_appointments = cur.fetchall()

        for appointment in all_appointments: 
            # Patient Replacement
            cur.execute(f'SELECT * FROM Patients WHERE patientID = {appointment["patientID"]};')
            single_patient = cur.fetchall()
            first_name = single_patient[0]['patientFirst']
            last_name = single_patient[0]['patientLast']
            patient_name = first_name + " " + last_name

            # Doctor Replacement 
            if appointment["doctorID"] != None:
                cur.execute(f'SELECT * FROM Doctors WHERE doctorID = {appointment["doctorID"]};')
                single_doc = cur.fetchall()
                doc_first = single_doc[0]["doctorFirst"]
                doc_last = single_doc[0]["doctorLast"]
                doctor_name = doc_first + " " + doc_last
                appointment["doctorID"] = doctor_name

            # Procedure Replacement
            cur.execute(f'SELECT * FROM Procedures WHERE procedureID = {appointment["procedureID"]};')
            single_procedure = cur.fetchall()
            procedure_name = single_procedure[0]["procedureName"]


            appointment["procedureID"] = procedure_name
            appointment["patientID"] = patient_name
        # Pass to the new template to be rendered
        return render_template('update_appts.html', appointment = this_appt, patient_list = all_patients, doctor_list = all_doctors, procedure_list = all_procedures)

    if table == 'procedures':
        # Get id for the chosen row
        this_procID = request.form['procedureID']

        # Get data for the chosen row
        query = f'SELECT * FROM Procedures WHERE procedureID={this_procID}'
        cur.execute(query)
        this_proc = cur.fetchone()

        # Pass to the new template to be rendered
        return render_template('update_procs.html', procedure = this_proc)

@app.route('/appointments', methods=['GET', 'POST', 'DELETE'])
def appointments():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Appointments')
        all_appointments = cur.fetchall()

        cur.execute('SELECT * FROM Patients')
        all_patients = cur.fetchall()

        cur.execute('SELECT * FROM Doctors')
        all_doctors = cur.fetchall()

        cur.execute('SELECT * FROM Procedures')
        all_procedures = cur.fetchall()

        for appointment in all_appointments: 
            # Patient Replacement
            cur.execute(f'SELECT * FROM Patients WHERE patientID = {appointment["patientID"]};')
            single_patient = cur.fetchall()
            first_name = single_patient[0]['patientFirst']
            last_name = single_patient[0]['patientLast']
            patient_name = first_name + " " + last_name

            # Doctor Replacement 
            if appointment["doctorID"] != None:
                cur.execute(f'SELECT * FROM Doctors WHERE doctorID = {appointment["doctorID"]};')
                single_doc = cur.fetchall()
                doc_first = single_doc[0]["doctorFirst"]
                doc_last = single_doc[0]["doctorLast"]
                doctor_name = doc_first + " " + doc_last
                appointment["doctorID"] = doctor_name

            # Procedure Replacement
            cur.execute(f'SELECT * FROM Procedures WHERE procedureID = {appointment["procedureID"]};')
            single_procedure = cur.fetchall()
            procedure_name = single_procedure[0]["procedureName"]


            appointment["procedureID"] = procedure_name
            
            appointment["patientID"] = patient_name

        mysql.connection.commit()
        return render_template('appointments.html', appointment_list=all_appointments, patient_list = all_patients, doctor_list = all_doctors, procedure_list=all_procedures)

    if request.method == "POST": 
        mode = request.form['mode']

        
        patientID = request.form['patientID']
        doctorID = request.form['doctorID']
        procedureID = request.form['procedureID']
        appointmentDate = request.form['appointmentDate']

        cur = mysql.connection.cursor()
        
        if mode == 'add':
            cur.execute(f'INSERT INTO Appointments (patientID, doctorID, procedureID, appointmentDate) VALUES ("{patientID}", "{doctorID}", "{procedureID}", "{appointmentDate}")')
        
        else:
            appointmentID = request.form['appointmentID']
            update_query = f'UPDATE Appointments SET patientID="{patientID}", doctorID="{doctorID}", procedureID="{procedureID}", appointmentDate="{appointmentDate}" WHERE appointmentID={appointmentID}'
            cur.execute(update_query)
        
        cur.execute('SELECT * FROM Appointments')
        all_appointments = cur.fetchall()

        cur.execute('SELECT * FROM Patients')
        all_patients = cur.fetchall()

        cur.execute('SELECT * FROM Doctors')
        all_doctors = cur.fetchall()

        cur.execute('SELECT * FROM Procedures')
        all_procedures = cur.fetchall()

        for appointment in all_appointments: 
            # Patient Replacement
            cur.execute(f'SELECT * FROM Patients WHERE patientID = {appointment["patientID"]};')
            single_patient = cur.fetchall()
            first_name = single_patient[0]['patientFirst']
            last_name = single_patient[0]['patientLast']
            patient_name = first_name + " " + last_name

            # Doctor Replacement 
            if appointment["doctorID"] != None:
                cur.execute(f'SELECT * FROM Doctors WHERE doctorID = {appointment["doctorID"]};')
                single_doc = cur.fetchall()
                doc_first = single_doc[0]["doctorFirst"]
                doc_last = single_doc[0]["doctorLast"]
                doctor_name = doc_first + " " + doc_last
                appointment["doctorID"] = doctor_name

            # Procedure Replacement
            cur.execute(f'SELECT * FROM Procedures WHERE procedureID = {appointment["procedureID"]};')
            single_procedure = cur.fetchall()
            procedure_name = single_procedure[0]["procedureName"]


            appointment["procedureID"] = procedure_name
            
            appointment["patientID"] = patient_name

        mysql.connection.commit()
        return render_template('appointments.html', appointment_list=all_appointments, patient_list = all_patients, doctor_list = all_doctors, procedure_list=all_procedures)

@app.route('/addresses', methods=['GET','PUT', 'POST', 'DELETE'])
def addresses():
    if request.method == 'GET': 
        cur = mysql.connection.cursor()
        
        cur.execute('SELECT * FROM Addresses')
        all_addresses = cur.fetchall()
        mysql.connection.commit()
        return render_template('addresses.html', address_list = all_addresses)

    if request.method == "POST":

        mode = request.form['mode']

        cur = mysql.connection.cursor()
        
        streetAddress= request.form['streetAddress']
        city = request.form['city']
        state = request.form['state']
        zipCode = request.form['zipCode']
        
        if mode == "add":
            cur.execute(f'INSERT INTO Addresses (streetAddress, city, state, zipCode) VALUES ("{streetAddress}", "{city}", "{state}", "{zipCode}")')
        
        else:
            # get values from request
            addressID = request.form['addressID']
            # Build query
            update_query = f'UPDATE Addresses SET streetAddress="{streetAddress}", city="{city}", state="{state}", zipCode="{zipCode}" WHERE addressID={addressID}'

            # make query
            cur.execute(update_query)

        cur.execute('SELECT * FROM Addresses')
        all_addresses = cur.fetchall()
        mysql.connection.commit()
        return render_template('addresses.html', address_list = all_addresses)

@app.route('/doctors-procedures', methods=['GET', 'PUT', 'POST', 'DELETE'])
def doctors_procedures():
    if request.method == 'GET': 
        cur = mysql.connection.cursor()
        
        cur.execute('SELECT * FROM Doctors_Procedures')
        all_doc_procs = cur.fetchall()

        cur.execute('SELECT * FROM Procedures')
        all_procedures = cur.fetchall()

        cur.execute('SELECT * FROM Doctors')
        all_doctors = cur.fetchall()

        for doc_proc in all_doc_procs: 

            # Doctor Replacement 
            cur.execute(f'SELECT * FROM Doctors WHERE doctorID = {doc_proc["doctorID"]};')
            single_doc = cur.fetchall()
            doc_first = single_doc[0]["doctorFirst"]
            doc_last = single_doc[0]["doctorLast"]
            doctor_name = doc_first + " " + doc_last

            # Procedure Replacement
            cur.execute(f'SELECT * FROM Procedures WHERE procedureID = {doc_proc["procedureID"]};')
            single_procedure = cur.fetchall()
            procedure_name = single_procedure[0]["procedureName"]

            doc_proc["procedureID"] = procedure_name
            doc_proc["doctorID"] = doctor_name

        mysql.connection.commit()
        return render_template('doctors_procedures.html', doc_proc_list=all_doc_procs, procedure_list = all_procedures, doctor_list = all_doctors)

    if request.method == "POST":

        procedureID= request.form['procedureID']
        doctorID = request.form['doctorID']
        
        cur = mysql.connection.cursor()

        cur.execute(f'INSERT INTO Doctors_Procedures (procedureID, doctorID) VALUES ("{procedureID}", "{doctorID}")')
       
        cur = mysql.connection.cursor()
        
        cur.execute('SELECT * FROM Doctors_Procedures')
        all_doc_procs = cur.fetchall()

        cur.execute('SELECT * FROM Doctors')
        all_doctors = cur.fetchall()

        cur.execute('SELECT * FROM Procedures')
        all_procedures = cur.fetchall()

        for doc_proc in all_doc_procs: 

            # Doctor Replacement 
            cur.execute(f'SELECT * FROM Doctors WHERE doctorID = {doc_proc["doctorID"]};')
            single_doc = cur.fetchall()
            doc_first = single_doc[0]["doctorFirst"]
            doc_last = single_doc[0]["doctorLast"]
            doctor_name = doc_first + " " + doc_last

            # Procedure Replacement
            cur.execute(f'SELECT * FROM Procedures WHERE procedureID = {doc_proc["procedureID"]};')
            single_procedure = cur.fetchall()
            procedure_name = single_procedure[0]["procedureName"]

            doc_proc["procedureID"] = procedure_name
            doc_proc["doctorID"] = doctor_name

        mysql.connection.commit()
        return render_template('doctors_procedures.html', doc_proc_list=all_doc_procs, procedure_list = all_procedures, doctor_list =  all_doctors)


# Listener

if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 55557))
    # app.run(port=12345, debug= True)
    # app.run(host="flip1.engr.oregonstate.edu", port=51515, debug=False) 

    app.run()
    # app.run(debug=True)