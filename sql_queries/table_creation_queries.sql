CREATE TABLE Addresses(addressID int(11) AUTO_INCREMENT PRIMARY KEY,streetAddress VARCHAR(80) NOT NULL,city VARCHAR(80) NOT NULL,state VARCHAR(80) NOT NULL,zipCode VARCHAR(80) NOT NULL);

CREATE TABLE Procedures(procedureID int(11) AUTO_INCREMENT PRIMARY KEY,procedureName VARCHAR(80) NOT NULL,inPatient BOOLEAN NOT NULL DEFAULT 0);

CREATE TABLE Departments(departmentID int(11) AUTO_INCREMENT PRIMARY KEY,departmentName VARCHAR(80) NOT NULL,departmentHead int(11),addressID int(11) NOT NULL,FOREIGN KEY (addressID) REFERENCES Addresses(addressID));

CREATE TABLE Doctors(doctorID int(11) AUTO_INCREMENT PRIMARY KEY,doctorFirst VARCHAR(80) NOT NULL,doctorLast VARCHAR(80) NOT NULL,doctorDOB DATE NOT NULL,departmentID int(11) NOT NULL,FOREIGN KEY (departmentID) REFERENCES Departments(departmentID));

-- This must be done as an alteration after Doctors is created, because Doctors must exist for the FOREIGN KEY statement to reference it.
ALTER TABLE Departments ADD FOREIGN KEY (departmentHead) REFERENCES Doctors(doctorID);

CREATE TABLE Patients(patientID int(11) AUTO_INCREMENT PRIMARY KEY,patientFirst VARCHAR(80) NOT NULL,patientLast VARCHAR(80) NOT NULL,patientDOB DATE NOT NULL,patientDoc int(11),FOREIGN KEY (patientDoc) REFERENCES Doctors(doctorID));

CREATE TABLE Appointments(appointmentID int(11) AUTO_INCREMENT PRIMARY KEY,patientID int(11) NOT NULL,doctorID int(11) NOT NULL,procedureID int(11) NOT NULL,appointmentDate DATE NOT NULL,FOREIGN KEY (patientID) REFERENCES Patients(patientID),FOREIGN KEY (doctorID) REFERENCES Doctors(doctorID),FOREIGN KEY (procedureID) REFERENCES Procedures(procedureID));

CREATE TABLE Doctors_Procedures(procedureID int(11) NOT NULL,doctorID int(11) NOT NULL,FOREIGN KEY (procedureID) REFERENCES Procedures(procedureID),FOREIGN KEY (doctorID) REFERENCES Doctors(doctorID));