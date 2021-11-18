------------------------------------------- Patients page -------------------------------------------
-----------------------------------------------------------------------------------------------------

-- Update Patient from patientID
UPDATE Patients SET patientFirst = :patientFirstUpdate, patientLast = :patientLastUpdate, patientDOB = :patientDOBUpdate, doctorID = :doctorIDUpdate WHERE patientID = :patientUpdateID

-- Add Patient 
INSERT INTO Patients (patientFirst, patientLast, patientDOB, patientDoc) VALUES (:patientFirstAdd, :patientLastAdd, :patientDOBAdd, :doctorIDAdd)

-- Get Patient first and last name for patient Dropdown
SELECT patientFirst, patientLast FROM Patients

-- Delete patient by id 
DELETE FROM Patients WHERE patientID = :patientIDSelected

------------------------------------------- Doctors page -------------------------------------------
-----------------------------------------------------------------------------------------------------

-- Update Doctor from doctorID
UPDATE Doctors SET doctorFirst = :doctorFirstUpdate, doctorLast = :doctorLastUpdate, doctorDOB = :doctorDOBUpdate, departmentID = :departmentIDUpdate WHERE doctorID = :doctorUpdateID

-- Add Doctor
INSERT INTO Doctors (doctorFirst, doctorLast, doctorDOB, departmentID) VALUES (:doctorFirstAdd, :doctorLastAdd, :doctorDOBAdd, :departmentIDAdd)

-- Delete doctor by id 
DELETE FROM Doctors WHERE doctorID = :doctorIDSelected

------------------------------------------- Procedures page -------------------------------------------
-----------------------------------------------------------------------------------------------------

-- Update Procedure from procedureID
UPDATE Procedures SET procdureName = :procedureNameUpdate, inPatient = :inPatientUpdate WHERE  procedureID = :procedureIDUpdate

-- Add procedure
INSERT INTO Procedures (prcedureName, inPatient) VALUES (:procedureNameAdd, :inpatientAdd)

-- Delete procedure by id 
DELETE FROM Procedures WHERE procedureID = :procedureIDSelected

------------------------------------------- Departments page -------------------------------------------
-----------------------------------------------------------------------------------------------------

-- Update Department from departmentID
UPDATE Departments SET departmentName = :departmentNameUpdate, departmentHead = :departmentHeadUpdate, addressID = :updateDepartmentAddress WHERE  departmentID = :departmentIDUpdate

-- Dropdown to find addresses 
SELECT streetAddress, city, state, zipCode FROM Addresses

-- Add Department
INSERT INTO Departments (departmentName, departmentHead, addressID) VALUES (:departmentNameAdd, :departmentHeadAdd, :departmentAddressAdd)

-- Delete Department by id 
DELETE FROM Departments WHERE departmentID= :departmentIDSelected

------------------------------------------- Appointments page -------------------------------------------
-----------------------------------------------------------------------------------------------------

-- Update Appointments from appointmentsID
UPDATE Appointments SET doctorID = :doctorIDUpdate, procedureID = :procedureIDUpdate, appointmentDate = :appointmentDateUpdate WHERE  appointmentID = :appointmentIDUpdate

-- Dropdown to find patients 
SELECT patientFirst, patientLast, patientID FROM Patients

-- Dropdown to find doctor
SELECT doctorFirst, doctorLast, doctorID FROM Doctors

-- Dropdown to find Procedure 
SELECT procedureName, procedureID FROM Procedures 

-- Add Appointment
INSERT INTO Appointments (patientID, doctorID, procedureID, appointmentDate) VALUES (:patientIDAdd, :doctorIDAdd, :procedureIDAdd, appointmentDateAdd)

-- Delete Appointment by id 
DELETE FROM Appointments WHERE appointmentID = :appointmentIDSelected

------------------------------------------- Addresses page -------------------------------------------
-----------------------------------------------------------------------------------------------------

-- Update Address from addressID
UPDATE Addresses SET streetAddress = :streetAddressUpdate, city = :cityUpdate, state = :stateUpdate, zipCode = :zipCodeUpdate WHERE addressID = :addressIDUpdate

-- Add address
INSERT INTO Addresses (streetAddress, city, state, zipCode) VALUES (:streetAddressAdd, :cityAdd, :stateAdd, :zipCodeAdd)

-- Delete address by id 
DELETE FROM Addresses WHERE addressID = :addressIDSelected


------------------------------------------- Doctors-procedures page -------------------------------------------
-----------------------------------------------------------------------------------------------------

-- Select Doctor name for dropdown
SELECT doctorFirst, doctorLast, doctorID FROM Doctors 

-- Select Procedure name for dropdown
SELECT procedureName, procedureID from Procedures

-- Add relationship between Doctor/Procedure 
INSERT INTO Doctors_Procedures (procedureID, doctorID) VALUES (:procedureIDSelected, :doctorIDSelected)

-- Delete Doctor/Procedure relationship
DELETE FROM Doctors_Procedures WHERE procedureID = :procedureIDSelected