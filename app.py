from flask import Flask, render_template
import os

# Configuration
 
app = Flask(__name__)

# Routes 

@app.route('/')
def root():
    return render_template('home.html')

@app.route('/doctors', methods=['PUT', 'POST', 'DELETE'])
def doctors():
    return render_template('doctors.html')

@app.route('/patients', methods=['PUT', 'POST', 'DELETE'])
def tutorial():
    return render_template('patients.html')

@app.route('/procedures', methods=['PUT', 'POST', 'DELETE'])
def tutorial():
    return render_template('procedures.html')

@app.route('/departments', methods=['PUT', 'POST', 'DELETE'])
def tutorial():
    return render_template('departments.html')

@app.route('/appointments', methods=['PUT', 'POST', 'DELETE'])
def tutorial():
    return render_template('appointments.html')

@app.route('/doctors-procedures', methods=['PUT', 'POST', 'DELETE'])
def tutorial():
    return render_template('doctors_procedures.html')

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    
    app.run(port=port, debug=True) 