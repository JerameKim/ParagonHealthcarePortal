
SET FOREIGN_KEY_CHECKS=0;

-- ############# Addresses
DROP TABLE IF EXISTS `Addresses`;
CREATE TABLE `Addresses` (
-- `addressID` int(11) AUTO_INCREMENT PRIMARY KEY,
`addressID` int(11) NOT NULL AUTO_INCREMENT,
`streetAddress` VARCHAR(80) NOT NULL,
`city` VARCHAR(80) NOT NULL,
`state` VARCHAR(80) NOT NULL,
`zipCode` VARCHAR(80) NOT NULL,
PRIMARY KEY (`addressID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- # Insert Addresses
INSERT INTO Addresses (`streetAddress`, `city`, `state`, `zipCode`) VALUES 
("123 Party Street","Cool Town", "WA", "54321"), 
("999 Random House Lane","Wherever", "GA", "01010"), 
("1 More Court","Beverly Hills", "WI", "44444");

-- ############# Procedures
DROP TABLE IF EXISTS `Procedures`;
CREATE TABLE `Procedures`(
    `procedureID` int(11) AUTO_INCREMENT PRIMARY KEY,
    `procedureName` VARCHAR(80) NOT NULL,
    `inPatient` BOOLEAN NOT NULL DEFAULT 0);

-- # INSERT PROCEDURES
-- LOCK TABLES `Procedures` WRITE; 
INSERT INTO `Procedures` (`procedureName`, `inPatient`) VALUES 
("Eyebrow Removal", 1),
("Eyebrow Addition", 1),
("Aura Manipulation", 0);
-- UNLOCK TABLES;

-- ############# Departments
DROP TABLE IF EXISTS `Departments`;
CREATE TABLE `Departments`(
    `departmentID` int(11) AUTO_INCREMENT PRIMARY KEY,
    `departmentName` VARCHAR(80) NOT NULL,
    `departmentHead` int(11),
    `addressID` int(11) NOT NULL,
    FOREIGN KEY (`addressID`) 
    REFERENCES `Addresses`(`addressID`));
        -- ON DELETE SET NULL
        -- ON UPDATE CASCADE);

-- # INSERT Departments
-- LOCK TABLES `Departments` WRITE; 
INSERT INTO `Departments` (`departmentName`, `departmentHead`, `addressID`) VALUES 
("Bone Department", NULL, 1), 
("Main Surgery", NULL, 2),
("Pharmacy", NULL, 2);
-- UNLOCK TABLES;

-- ############# Doctors
DROP TABLE IF EXISTS `Doctors`;
CREATE TABLE `Doctors`(
    `doctorID` int(11) AUTO_INCREMENT PRIMARY KEY,
    `doctorFirst` VARCHAR(80) NOT NULL,
    `doctorLast` VARCHAR(80) NOT NULL,
    `doctorDOB` DATE NOT NULL,
    `departmentID` int(11) NOT NULL,
    FOREIGN KEY (`departmentID`) REFERENCES `Departments`(`departmentID`));
        -- ON DELETE SET NULL
        -- ON UPDATE CASCADE);
-- # INSERT Doctors 
-- LOCK TABLES `Doctors`; 
INSERT INTO `Doctors` (`doctorFirst`, `doctorLast`, `doctorDOB`, `departmentID`) VALUES 
("Dorian", "Grey", "1999-09-09", 1), 
("Frasier", "Crane", "2000-01-01", 2),
("Simon", "Garfunkle", "2040-11-11", 2);
-- UNLOCK TABLES;

-- This must be done as an alteration after Doctors is created, because Doctors must exist for the FOREIGN KEY statement to reference it.
ALTER TABLE `Departments` ADD FOREIGN KEY (`departmentHead`) REFERENCES `Doctors`(`doctorID`);

-- ############# Patients
DROP TABLE IF EXISTS `Patients`;
CREATE TABLE `Patients`(
    `patientID` int(11) AUTO_INCREMENT PRIMARY KEY,
    `patientFirst` VARCHAR(80) NOT NULL,
    `patientLast` VARCHAR(80) NOT NULL,
    `patientDOB` DATE NOT NULL,
    `patientDoc` int(11),
    FOREIGN KEY (`patientDoc`) REFERENCES `Doctors`(`doctorID`) );
        -- ON DELETE SET NULL
        -- ON UPDATE CASCADE);
-- LOCK TABLES `Patients`;
INSERT INTO Patients (patientFirst, patientLast, patientDOB, patientDoc) VALUES 
("Zachary","Zucchini", "1994-12-12", 1),
("Andrew","Armadillo", "1983-05-03", 1),
("Sally","Ride", "1951-05-26", 2);
-- UNLOCK TABLES;

-- ############# Appointments
DROP TABLE IF EXISTS `Appointments`;
CREATE TABLE `Appointments`(
    `appointmentID` int(11) AUTO_INCREMENT PRIMARY KEY,
    `patientID` int(11) NOT NULL,
    `doctorID` int(11) NOT NULL,
    `procedureID` int(11) NOT NULL,
    `appointmentDate` DATE NOT NULL,
    FOREIGN KEY (`patientID`) REFERENCES `Patients`(`patientID`),
        -- ON DELETE SET NULL
        -- ON UPDATE CASCADE,
    FOREIGN KEY (`doctorID`) REFERENCES `Doctors`(`doctorID`), 
        -- ON DELETE SET NULL 
        -- ON UPDATE CASCADE,
    FOREIGN KEY (`procedureID`) REFERENCES `Procedures`(`procedureID`));
        -- ON DELETE SET NULL
        -- ON UPDATE CASCADE);
-- LOCK TABLES `Appointments`;
INSERT INTO `Appointments` (`patientID`, `doctorID`, `procedureID`, `appointmentDate`) VALUES 
(1, 1, 1, "2000-10-10");
-- UNLOCK TABLES; 

-- ############# Doctors_Procedures
DROP TABLE IF EXISTS `Doctors_Procedures`;
CREATE TABLE `Doctors_Procedures`(
    `procedureID` int(11) NOT NULL,
    `doctorID` int(11) NOT NULL,
    FOREIGN KEY (`procedureID`) REFERENCES `Procedures`(`procedureID`),
        -- ON DELETE SET NULL 
        -- ON UPDATE CASCADE,
    FOREIGN KEY (`doctorID`) REFERENCES `Doctors`(`doctorID`));
        -- ON DELETE SET NULL
        -- ON UPDATE CASCADE);
-- LOCK TABLES `Doctors_Procedures`;
INSERT INTO Doctors_Procedures (procedureID, doctorID) VALUES 
(1, 1);
-- UNLOCK TABLES;

SET FOREIGN_KEY_CHECKS=1;

-- ######## Sample data ######## -- 
    -- # Insert Addresses
-- INSERT INTO Addresses (streetAddress, city, state, zipCode) VALUES ("123 Party Street","Cool Town", "WA", "54321");
-- INSERT INTO Addresses (streetAddress, city, state, zipCode) VALUES ("999 Random House Lane","Wherever", "GA", "01010");
-- INSERT INTO Addresses (streetAddress, city, state, zipCode) VALUES ("1 More Court","Beverly Hills", "WI", "44444");


    -- # Insert Procedures 
-- INSERT INTO Procedures (procedureName, inPatient) VALUES ("Eyebrow Removal", 1);
-- INSERT INTO Procedures (procedureName, inPatient) VALUES ("Eyebrow Addition", 1);
-- INSERT INTO Procedures (procedureName, inPatient) VALUES ("Aura Manipulation", 0);

    -- # Insert Departments
-- INSERT INTO Departments (departmentName, departmentHead, addressID) VALUES ("Bone Department", NULL, 1);
-- INSERT INTO Departments (departmentName, departmentHead, addressID) VALUES ("Main Surgery", NULL, 2);
-- INSERT INTO Departments (departmentName, departmentHead, addressID) VALUES ("Pharmacy", NULL, 2);

    -- # Insert Some Doctors
-- INSERT INTO Doctors (doctorFirst, doctorLast, doctorDOB, departmentID) VALUES ("Dorian", "Grey", "1999-09-09", 1);
-- INSERT INTO Doctors (doctorFirst, doctorLast, doctorDOB, departmentID) VALUES ("Frasier", "Crane", "2000-01-01", 2);
-- INSERT INTO Doctors (doctorFirst, doctorLast, doctorDOB, departmentID) VALUES ("Simon", "Garfunkle", "2040-11-11", 2);

    -- # Insert Patients
-- INSERT INTO Patients (patientFirst, patientLast, patientDOB, patientDoc) VALUES ("Zachary","Zucchini", "1994-12-12", 1);
-- INSERT INTO Patients (patientFirst, patientLast, patientDOB, patientDoc) VALUES ("Andrew","Armadillo", "1983-05-03", 1);
-- INSERT INTO Patients (patientFirst, patientLast, patientDOB, patientDoc) VALUES ("Sally","Ride", "1951-05-26", 2);

    -- # Insert Doctors_Procedures
-- INSERT INTO Doctors_Procedures (procedureID, doctorID) VALUES (1, 1);

    -- # Insert Appointments
-- INSERT INTO Appointments (patientID, doctorID, procedureID, appointmentDate) VALUES (1, 1, 1, "2000-10-10");