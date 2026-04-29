CREATE TABLE drivers (driver_id INT, forename VARCHAR(100), surname VARCHAR(100), nationality VARCHAR(100), dob DATE);
CREATE TABLE driverstandings (driver_id INT, race_id INT);
CREATE TABLE races (race_id INT, name VARCHAR(100));
