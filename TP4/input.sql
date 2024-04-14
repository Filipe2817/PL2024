Select id, nome, salario From empregados Where salario >= 820

CREATE TABLE Departments (
    DepartmentID INT PRIMARY KEY,
    DepartmentName VARCHAR(50) NOT NULL
);

INSERT INTO Departments (DepartmentID, DepartmentName) VALUES (1, 'IT');
INSERT INTO Departments (DepartmentID, DepartmentName) VALUES (2, 'HR');
INSERT INTO Departments (DepartmentID, DepartmentName) VALUES (3, 'Finance');

UPDATE Departments SET DepartmentName = 'Information Technology' WHERE DepartmentID = 1;

DELETE FROM Departments WHERE DepartmentID = 2;

SELECT * FROM Departments LIMIT 5;

CREATE TABLE Employee (
    EmployeeID INT PRIMARY KEY,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(50),
    DepartmentID INT,
    Salary DECIMAL(10, 2) DEFAULT 820.00,
    CONSTRAINT FK_Department FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

INSERT INTO Employee (EmployeeID, FirstName, LastName, DepartmentID, Salary) 
VALUES (1, 'John', 'Doe', 1, 60000.00);

INSERT INTO Employee (EmployeeID, FirstName, LastName, DepartmentID, Salary) 
VALUES (3, 'Michael', 'Johnson', 3, 65000.00);

SELECT * FROM Employee WHERE DepartmentID = 1;

SELECT e.EmployeeID, e.FirstName, e.LastName, d.DepartmentName 
FROM Employee e 
JOIN Departments d ON e.DepartmentID = d.DepartmentID;

SELECT d.DepartmentName, AVG(e.Salary) AS AverageSalary 
FROM Employee e 
JOIN Departments d ON e.DepartmentID = d.DepartmentID 
GROUP BY d.DepartmentName;

SELECT * FROM Employee 
WHERE Salary = (SELECT MAX(Salary) FROM Employee);

SELECT * FROM Employee 
WHERE DepartmentID = 1 AND Salary > 50000.00 
ORDER BY Salary DESC;
