CREATE VIEW ConstructorEmployeeOverFifty AS SELECT Employee.* , ConstructorEmployee.CompanyName,ConstructorEmployee.SalaryPerDay
FROM Employee LEFT OUTER JOIN ConstructorEmployee
	ON Employee.EID=ConstructorEmployee.EID
	WHERE (strftime('%Y', 'now') + strftime('%j', 'now') / 365) - (strftime('%Y', Employee.BirthDate) + strftime('%j', Employee.BirthDate) / 365)>=50;
CREATE VIEW ApartmentNumberInNeighborhood AS SELECT Neighborhood.NID, count(*) AS ApartmentNumber
FROM Neighborhood LEFT OUTER JOIN Apartment
	ON Neighborhood.NID=Apartment.NID
	GROUP BY Neighborhood.NID;



-- Add Triggers Here, do not forget to separate the triggers with ;
CREATE TRIGGER trig_1
AFTER DELETE ON Project
BEGIN
	DELETE FROM ConstructorEmployee WHERE EID IN (SELECT EID FROM ProjectConstructorEmployee GROUP BY EID HAVING PID=OLD.PID AND COUNT(PID)=1 );
	DELETE FROM Employee WHERE EID NOT IN (SELECT EID FROM OfficialEmployee UNION SELECT EID FROM ConstructorEmployee);
END;

CREATE TRIGGER two_manager_per_department
BEFORE INSERT ON Department
BEGIN
	SELECT CASE 
		WHEN NEW.ManagerID IN (SELECT ManagerID FROM Department 
		GROUP BY Department.ManagerID
		HAVING count(Department.ManagerID)  >= 2 )
	THEN RAISE (ABORT , 'Manager can manage up to two depatments.')
	END;
END;