# SQL CREATE DATABASE Statement
---
* 관리자권한이 있는 User만 사용 가능 하다.
* 새 SQL DATABASE를 만들때 사용
```
-- testDB라는 이름의 DB를 만든다.
CREATE DATABASE testDB
```
<br>

# SQL DROP DATABASE Statment
---
* 기존 SQL DATABASE를 삭제 할때 사용.
```
-- testDB라는 이름의 DB를 삭제 한다.
DROP DATABASE testDB;
```
* 데이터베이스를 삭제하기 전에 관리자 권한이 있어야합니다.
데이터베이스가 삭제되면 다음 SQL 명령을 사용하여 데이터베이스 목록에서 데이터베이스를 확인할 수 있습니다.
`SHOW DATABASES;`
<br>

# SQL CREATE TABLE Statement
---
* DB에 새 테이블을 만들때 사용.
```
-- Persons라는 이름의 테이블을 만드나
-- columns는 정수형 PersonID와 문자형(255개)를 가지는 LastName, FirstName, Address, City를 가진다.
CREATE TABLE Persons {
	PersonID int,
	LastName varchar(255),
	FirstName varchar(255),
	Address varchar(255),
	City varchar(255),
}
```
* 다른 테이블을 사용하여 새 테이블 만들기
	* CREATE TABLE과 SELECT를 조합하여 사용.
	* 특정 column이나 모든 column을 가져 올 수 있다.
	* 기존 테이블을 사용하여 새 테이블을 만들면 새 테이블의 값은 기존 테이블의 값으로 채워져 있다.
```
-- 새로운 테이블을 다른 테이블에서 조건에 맞는 columns를 가져와서 만들수 있다.
CREATE TABLE new_table_name AS
	SELECT column1, column2, ...
	FROM existing_table_name
	WHERE ...;
```
<br>

# SQL DROP TABLE Statement
---
* 기존 테이블을 삭제 하는데 사용.
```
-- Shippers테이블 삭제
DROP TABLE Shippers;
```
* SQL TRUNCATE TABLE
	* 해당 테이블의 데이터만 삭제 하고 테이블 자체는 삭제 하지 않는다.
```
TRUNCATE TABLE table_name;
```
<br>

# SQL ALTER TABLE Statement
---
* 기존 테이블에 column을 추가 하거나 삭제, 수정 할때 사용 한다.
* 기존 테이블에 다양한 제약조건을 없애거나 넣을때 사용 한다.
```
-- Persons테이블에 DateOfBirth column을 date형으로 추가함.
ALTER TABLE Persons
ADD DateOfBirth date;
```
```
-- Persons테이블의 DateOfBirth column을 year형으로 변경함.
ALTER TABLE Persons
-- Ms Access
ALTER COLUMN DateOfBirth year;
-- My d
MODIFY COLUMN DateOfBirth year;
-- Oracle
MODIFY DateOfBirth year;
```
```
-- Persons테이블의 DateOfBirth column을 삭제 함.
ALTER TABLE Persons
DROP COLUMN DateOfBirth;
```
<br>

# SQL Constraints
---
* 테이블의 데이터에 대한 규칙을 지정 하기 위해 사용.
* CREATE TABLE 이나 ALTER TABLE로 테이블이 작성 된 후에 제한 조건을 지정 할 수 있다.
```
CREATE TABLE table_name {
	column_name1 data_type constraint,
	column_name2 data_type constraint,
	column_name3 data_type constraint,
}
```
* 데이터가 들어 갈수 있는 데이터 유형을 제한하는데 사용. 이렇게 하면 표데이터의 정확성과 신뢰성이 보장됨.
* 제한조건과 데이터 작업사이에 위반된 제한조건이 있으면 작업이 중단됨.
* 제약조건은 Columns나 Table전체에 적용 할 수 있다,
	* NOT NULL - column이 NULL을 가질 수 없음을 지정.
	* UNIQUE - column의 값들이 서로 중복되지 않게 지정.
	* PRIMARY KEY - NOT NULL과 UNIQUE의 조합으로 테이블의 각 column을 고유하게 식별하게 함.
	* FOREIGN KEY - 다른 테이블의 row/column을 고유하게 식별함.
	* CHECK - column의 모든값이 특정 조건을 충족하는지 확인.
	* DEFAULT - 값이 지정 되지 않는 경우 column에 기본값을 지정.
	* INDEX - DB에서 데이터를 매우 신속하게 생성및 검색하는데 사용.
<br>

# SQL NOT NULL Constraints
---
* 기본적으로 column은 Null값을 포함 할 수 있다.
* column이 Null을 가질수 없게 함.
* 이렇게 하면 필드에 항상 값이 포함되게 할 수 있다. 즉 데이터를 새로 삽입하거나 업데이트 할때 필드에 값을 넣지 않고는 할수 없다.
```
CREATE TABLE Persons {
	ID int NOT NULL, -- Null을 가질수 없다.
	LastName varchar(255) NOT NULL, -- Null을 가질수 없다.
	FirstName varchar(255) NOT NULL, -- Null을 가질수 없다.
	Age int -- Null을 가질수 있다.
};
```
<br>

# SQL UNIQUE Constraints
---
* 열의 모든값이 서로 다른지 확인.
* UNIQUE 및 PRIMARY KEY는 column의 값의 고유함을 보장한다.
* PRIMARY KEY는 자동으로 UNIQUE가 자동으로 제약조건에 포함된다.
* UNIQUE는 테이블당 여러 column에 제약조건을 걸수 있지만, PRIMARY KEY는 테이블당 하나만 걸 수 있다.
* SQL Server / Oracle / Ms Access
```
CREATE TABLE Persons {
	ID int NOT NULL UNIQUE,
	LastName varchar(255) NOT NULL,
	FirstName varchar(255),
	Age int
};
```
* My d
CREATE TABLE Persons {
	ID int NOT NULL,
	LastName varchar(255) NOT NULL,
	FirstName varchar(255),
	Age int,
	UNIQUE(ID)
};
* 여러 column에 UNIQUE 제약 조건을 설정 하는 방법.
* MySQL / SQL Server / Oracle / MS Access
```
CREATE TABLE Persons {
	ID int NOT NULL,
	LastName varchar(255) NOT NULL,
	FirstName varchar(255),
	Age int,
	CONSTRAINT UC_Person UNIQUE (ID, LastName)
}
```
* ALTER TABLE할때 UNIQUE 제약 조건 방법.
* 테이블이 이미 만들어 졌을때 UNIQUE제약 조건을 넣고 싶을때
```
ALTER TABLE Persons
ADD UNIQUE(ID);
```
* 테이블이 이미 만들어 졌을때 UNIQUE제약 조건에 이름을 지정하고 여러 column에 UNIQUE제약 조건을 넣고 싶을떄
```
ALTER TABLE Persons
ADD CONSTRAINT UC_Person UNIQUE (ID, LastName);
```

* UNIQUE 제약조건을 삭제 하고 싶을때
* 제약 조건 이름으로 삭제 한다.

* My d
```
ALTER TABLE Persons
DROP INDEX UC_Person;
```
* SQL Server / Oracle / Ms Access
```
ALTER TABLE Persons
DROP CONSTRAINT UC_Person;
```
<br>

# SQL PRIMARY KEY Constraint
---
* PEIMARY KEY는 UNIQUE 제약조건을 기본적으로 가지고 있다.
* UNIQUE값을 포함해야 하며 NULL값을 사용할 수 없다.
* 테이블에는 기본키가 하나만 존재 해야 하며, 하나 또는 여러개의 필드로 구성 될 수 있다.
* My d
```
CREATE TABLE Persons (
	ID int NOT NULL,
	LastName varchar(255) NOT NULL,
	FirstName varchar(255),
	Age int,
	PRIMARY KEY (ID)
)
```
* SQL Server / Oracle / Ms Access
```
CREATE TABLE Persons (
	ID int NOT NULL PRIMARY KEY,
	LastName varchar(255) NOT NULL,
	FirstName varchar(255),
	Age int
);
```
* 여러 column에 대해 제약 조건을 설정 할때
```
-- Primary Key는 ID 하나이지만 ID+LastName 두개의 column으로 구성 되어 있다.
CREATE TABLE Persons (
	ID int NOT NULL,
	LastName varchar(255) NOT NULL,
	FirstName varchar(255),
	Age int,
	CONSTRAINT PK_Person PRIMARY KEY (ID, LastName)
)
```
* PRIMARY KEY 제약 조건 추가
```
-- ID에 PRIMARY KEY 제약조건을 검
ALTER TABLE Persons
ADD PRIMARY KEY (ID);
```
```
-- iD에 PRIMARY KEY 제약조건을 거는데 PRIMARY KEY 는 ID+LastName으로 구성됨
ALTER TABLE Persons
ADD CONSTRAINT PK_Person PRIMARY KEY (ID, LastName);
```
* ALTER TABLE 문을 사용하여 기본 키를 추가하는 경우 기본 키 열은 (테이블이 처음 작성되었을 때) NULL 값을 포함하지 않도록 이미 선언되어 있어야 한다.
* PRIMARY KEY 제약 조건 삭제
* My d
```
ALTER TABLE Persons
DROP PRIMARY KEY;
```
* SQL Server / Oracle / Ms Access
```
ALTER TABLE Persons
DROP CONSTRAINT PK_Person;
```
<br>

# SQL FOREIGN KEY Constraint
---
* 두 개의 테이블을 서로 연결할때 사용 함.
* 테이블에서 다른 테이블의 PRIMARY KEY와 연결 되는 필드(혹은 필드 모음).
* FOREIGN KEY가 들어 있는 테이블을 하위 테이블 이라 하고, 후보 키가 들어 있는 테이블을 참조된 테이블 또는 상위 테이블 이라 한다.
* 테이블을 만들때 FOREIGN KEY
* My d
```
CREATE TABLE Orders(
	OrderID int NOT NULL,
	OrderNumber int NOT NULL,
	PersonID int,
	PRIMARY KEY (OrderID),
	FOREIGN KEY (PersonID) REFERENCES Persons(PersonID)
);
```
* SQL Server / Oracle / Ms Access
```
CREATE TABLE Orders(
	OrderID int NOT NULL PRIMARY KEY,
	OrderNumber int NOT NULL,
	PersonID int FOREIGN KEY REFERENCES Persons(PersonID)
);

```
* FOREIGN KEY에 이름 지정및 여러 column에 제약 조건 설정
```
CREATE TABLE Orders(
	OrderID int NOT NULL,
	OrderNumber int NOT NULL,
	PersonID int,
	PRIMARY KEY (OrderID),
	CONSTRAINT FK_PersonOrder FOREIGN KEY (PersonID)
	REFERENCES Persons(PersonID)
);
```
* FOREIGN KEY 제약 조건 추가
```
ALTER TABLE Orders
ADD FOREIGN KEY (PersonID) REFERENCES Persons(PersonID);
```
* FOREIGN KEY 제약 조건 이름 지정 추가 및 여러 column에 제약 조건 설정
```
ALTER TABLE Orders
ADD CONSTRAINT FK_PersonOrder
FOREIGN KEY (PersonID) REFERENCES Persons(PersonID);
```
* FOREIGN KEY 제약 조건 삭제
* My d
```
ALTER TABLE Orders
DROP FOREIGN KEY FK_PersonOrder;
```
* SQL Server / Oracle / Ms Access
```
ALTER TABLE Orders
DROP CONSTRAINT FK_PersonOrder;
```
<br>

# SQL CHECK Constraint
---
* column에 넣을수 있는 값의 범위를 제한하는데 사용.
* 특정 column에 지정 하게 되면 해당 column에만 특정 된다.
* 테이블에 지정 하면 ROW 전체에 영향을 준다.
* 테이블을 만들때
* My d
```
CREATE TABLE Persons(
	ID int NOT NULL,
	LastName varchar(255) NOT NULL,
	FirstName varchar(255),
	Age int,
	CHECK (Age>=18)
);
```
* SQL Server / Oracle / Ms Access
```
CREATE TABLE Persons(
	ID int NOT NULL,
	LastName varchar(255) NOT NULL,
	FirstName varchar(255),
	Age int CHECK (Age>=18)
);
```
* 두개 이상의 CHECK Constraint를 지정 할때와 이름을 부여 할때
```
CREATE TABLE Persons(
	ID int NOT NULL,
	LastName varchar(255) NOT NULL,
	FirstName varchar(255),
	Age int,
	City varchar(255),
	CONSTRAINT CHK_Person CHECK (Age>=18 AND City='Sandnes')
);
```
* CHECK Constraint를 추가 할때
```
ALTER TABLE Persons
ADD CHECK(Age>=18);
```
* 두개 이상의 column에 CHECK Constraint를 추가 하고 이름을 지정 할때
```
ALTER TABLE Persons
ADD CONSTRAINT CHK_PersonAge CHECK (Age>=18 AND City='Sandnes')
```
* CHECK Constraint를 삭제 할때
* SQL Server / Oracle / Ms Access
```
ALTER TABLE Persons
DROP CONSTRAINT CHK_PersonAge;
```
* My d
```
ALTER TABLE Persons
DROP CHECK CHK_PersonsAge;
```
<br>

# SQL DEFAULT Constraint
---
* column의 기본 값을 제공하기위해 사용.
* 다른 값을 지정 하지 않으면 기본값으로 지정 한다.
* 테이블을 만들때
```
CREATE TABLE Persons(
	ID int NOT NULL,
	LastName varchar(255) NOT NULL,
	FirstName varchar(255),
	Age int,
	City varchar(255) DEFAULT 'Sandnes'
);
```
* DEFAULT는 함수를 사용하여 시스템 값을 넣어 줄 수도 있다.
```
CREATE TABLE Orders(
	ID int NOT NULL,
	OrderNumber int NOT NULL,
	OrderDate date DEFAULT GETDATE()
);
```
* DEFAULT Constraint 추가
* My sql
```
ALTER TABLE Persons
ALTER City SET DEFAULT 'Sandnes';
```
* SQL Server / Ms Access
```
ALTER TABLE Persons
ALTER COLUMN City SET DEFAULT 'Sandnes'
```
* Oracle
```
ALTER TABLE PPersons MODIFY City DEFAULT 'Sandnes'
```
* DEFAULT Constraint 삭제
* My d
```
ALTER TABLE Persons
ALTER City DROP DEFAULT;
```
* SQL Server / Oracle / Ms Access
```
ALTER TABLE Persons
ALTER COLUMN City DROP DEFAULT;
```
<br>

# SQL CREATE INDEX Statement
---
* 테이블에 index를 만드는 데 사용.
* index는 DB에서 데이터를 매우 빨리 검색 하는데 사용 하며, 사용 자는 index를 볼수 없으며 검색/쿼리의 속도를 높이기 위해 사용한다.
* index를 사용하여 테이블을 update 하는 것은 index를 update 해야 하기 때문에 느려진다. 따라서 자주 사용할 column에 대해서만 index를 적용하라.
* INDEX 만들기
```
CREATE INDEX idx_lastname
ON Persons (LastName);
```
```
CREATE INDEX idx_pname
ON Persons (LastName, FirstName);
```
* UNIQUE INDEX 만들기
```
CREATE UNIQUE INDEX idx_lastname
ON Persons (LastName);
```
* INDEX 삭제 하기
* Ms Access
```
DROP INDEX index_name ON table_name;
```
* SQL Server
```
DROP INDEX table_name.index_name;
```
* DB2/Oracle
```
DROP INDEX index_name;
```
* My d
```
ALTER TABLE table_name
DROP INDEX index_name
```
<br>

# SQL AUTO INCREMENT Field
---
* 테이블에 새로운 레코드를 추가 할때 UNIQUE한 번호가 자동으로 생성 되도록 함.
* 대부분의 테이블에 레코드를 추가 할때 PRIMARY KEY로 만들어진 필드가 이것 이다.
* My SQL
```
CREATE TABLE Persons(
	ID int NOT NULL AUTO_INCREMENT,
	LastName varchar(255) NOT NULL,
	FirstName varchar(255),
	Age int,
	PRIMARY KEY(ID)
)
```
* 기본 적으로 시작점은 1로 시작하여 1씩 증가 한다.
* 하지만 시작점을 바꿀 경우엔 이렇게 한다.
```
ALTER TABLE Persons AUTO_INCREMENT=100;
```
* Persons테이블에 새로운 레코드를 추가 할때 ID값을 지정 하지 않아도 알아서 지정 된다.
```
INSERT INTO Persons (FirstName, LastName)
VALUES ('Lars', 'Monsen');
```
* SQL Server
```
CREATE TABLE Persons (
	--ID int IDENTITY(10, 5) 10에서 5씩 증가
	ID int IDENTITY(1, 1) PRIMARY KEY,
	LastName varchar(255) NOT NULL,
	FirstName varchar(255),
	Age int
)
```
```
INSERT INTO Persons (FirstName, LastName)
VALUES ('Lars', 'Monsen');
```
* Ms Access
```
CREATE TABLE Persons(
	ID Integer PRIMARY KEY AUTOINCREMENT,
	LastName varchar(255) NOT NULL,
	FirstName varchar(255),
	Age int
);
```
```
INSERT INTO Persons (FirstName, LastName)
VALUES ('Lars', 'Monsen');
```
* Oracle
* SEQUENCE객체를 추가로 만들어서 객체를 이용하여 만들어 지는 숫자값을 DB에 삽입한다.
```
CREATE SEQUENCE seq_person
MINVALUE 1
START WITH 1
INCREMENT BY 1
CACHE 10;
```
```
INSERT INTO Persons (FirstName, LastName)
VALUES (seq_person.nextval, 'Lars', 'Monsen');
```
<br>

# SQL Working With Dates
---
* 날짜 형식을 사용함에 있어 가장 어려운일은 삽입하려는 날짜 형식이 DB에 날짜 column형식과 일치 하는지 확인하는 것.
* 데이터에 시간까지 들어가 있으면 복잡해 진다.
* SQL Date Data 유형
* My d에서 사용하는 날짜/날짜시간 형식
	* DATE - format YYYY-MM-DD
	* DATETIME - format: YYYY-MM-DD HH:MI:SS
	* TIMESTAMP - format: YYYY-MM-DD HH:MI:SS
	* YEAR - format YYYY or YY
* SQL Server에서 사용하는 날짜/날짜시간 형식
	* DATE - format YYYY-MM-DD
	* DATETIME - format: YYYY-MM-DD HH:MI:SS
	* SMALLDATETIME - format: YYYY-MM-DD HH:MI:SS
	* TIMESTAMP - format: a unique number
> 데이터 베이스 새 테이블을 만들때 column에 대해 date type이 선택 된다.
* 시간요소가 없으면 DATE비교가 쉽다.
```
CREATE TABLE Orders(
	OerderID int NOT NULL,
	ProductName varchar(100) NOT NULL,
	OrderDate datetime NOT NULL DEFAULT NOW(),
	PRIMARY KEY (OrderID)
);
```
```
-- OrderDate에 값을 지정 하지 않아도 DEFAULT NOW()덕분에 OrderDate column에 현재 날짜/시간이 들어 간다
INSERT INTO Orders (ProductName) VALUES ('Jarlsberg Cheese')
```
```
SELECT * FROM Orders WHERE OrderDate='2008-11-11'
```
* 시간 요소가 있으면 원하는 결과를 얻지 못한다.
* 쉽게 구성하려면 시간 요소는 없애는게 좋다.
<br>

# SQL VIEW Statement
---
* VIEW는 SQL구문에 의해서 만들어진 결과셋을 기초로한 가상 테이블이다.
* 진짜 테이블처럼 columns과 rows를 가진다. VIEW의 field는 실 DB에 있는 하나이상의 실제 테이블이다
* 함수, WHERE, JOIN 등을 할수 있다.
* VIEW는 항상 최신데이터를 유지 한다.
```
-- Products테이블에서 Discontinued가 No인
-- ProductID, ProductName columns을 가져와
-- Current Product List라는 이름의 가상의 VIEW를 만든다
CREATE VIEW [Current Product List] AS
SELECT ProductID, ProductName
FROM Products
WHERE Discontinued = No;
```
* 그리고 그 VIEW에 SQL문을 쿼리 할 수 있다.
```
SELECT * FROM [Current Product List];
```
```
-- UnitPrice가 전체 UnitPrice의 평균값보다 큰 ProductName, UnitPrice를 가져와 Products Above Price라는 이름의 VIEW로 만든다
CREATE VIEW [Products Above Price] AS
SELECT ProductName, UnitPrice
FROM Products
WHERE UnitPrice > (SELECT AVG(UnitPrice) FROM Products);
```
```
SELECT * FROM [Product Above Price];
```
```
CREATE VIEW [Category Sales For 1997] AS
SELECT DISTINCT CategoryName, Sum(ProductSales) AS CategorySales
FROM [Product sales for 1997]
GROUP BY CategoryName;
```
```
SELECT * FROM [Category Sales For 1997];
```
```
SELECT * FROM [Category Sales For 1997]
WHERE CategoryName='Beverages';
```
* VIEW 갱신
```
CREATE OR REPLACE VIEW view_name AS
SELECT column1, column2, ...
FROM table_name
WHERE condition;
```
```
CREATE OR REPLACE VIEW [Current Product List] AS
SELECT ProductID, ProductName, Category
FROM Products
WHERE Discontinued = No;
```
* VIEW 삭제
```
DROP VIEW view_name;
```
<br>

# SQL HOSTING
---
* 웹사이트에서 DB의 데이터를 저장/검색 할수 있게 하려면 웹 서버가 SQL언어를 사용하는 DB 시스템에 접근 할 수 있어야 한다,
* 웹 서버가 ISP (Internet Service Provider)에 의해 호스팅되는 경우 SQL 호스팅 plan을 찾아야 한다.
* 가장 일반적인 SQL 호스팅 DB는 MS SQL Server, Oracle, MySQL 및 MS Access입니다.
* MS SQL Server
> Microsoft의 SQL Server는 트래픽이 많은 데이터베이스 중심 웹 사이트에 널리 사용되는 데이터베이스 소프트웨어입니다. SQL Server는 강력하고 완벽한 SQL 데이터베이스 시스템입니다.

* Oracle
> 오라클은 트래픽이 많은 데이터베이스 중심 웹 사이트에 널리 사용되는 데이터베이스 소프트웨어이기도합니다. 오라클은 강력하고 강력한 SQL 데이터베이스 시스템입니다.

* MySQL
> MySQL은 웹 사이트에 널리 사용되는 데이터베이스 소프트웨어이기도합니다. MySQL은 강력하고 강력한 SQL 데이터베이스 시스템입니다. MySQL은 값 비싼 Microsoft 및 Oracle 솔루션 대신 저렴한 방법입니다.

* Access
> 웹 사이트에 단순한 데이터베이스 만 있으면 Microsoft Access가 솔루션이 될 수 있습니다. 액세스는 트래픽이 많고 MySQL, SQL Server 또는 Oracle만큼 강력하지는 않습니다.
<br>

# SQL FIRST()
---
* 해당 column의 첫번째 값 가져 오기
```
-- Ms Access
SELECT FIRST(CustomerName) AS FirstCustomer FROM Customers;
-- SQL Server
SELECT TOP 1 CustomerName FROM Customers ORDER BY CustomerID ASC;
-- My Sql
SELECT CustomerName FROM Cusotmers ORDER BY CustomerID ASC LIMIT 1;
-- Oracle
SELECT CustomerName FROM Cusotmers WHERE ROWNUM <= 1 ORDER BY CustomerID ASC;
```
<br>

# SQL LAST()
---
* 해당 column의 마지막 값 가져 오기
```
-- Ms Access
SELECT LAST(CustomerName) FROM Customers
-- SQL Server
SELECT TOP 1 CustomerName FROM Customers ORDER BY CustomerID DESC;
-- My Sql
SELECT CustomerName FROM Custoers ORDER BY CustomerID DESC LIMIT 1;
-- Oracle
SELECT CustomerName FROM Customers ORDER BY CustomerID DESC WHERE ROWNUM <= 1;
```
<br>

# SQL UCASE()
---
* field값을 대문자로 변환
```
-- General
SELECT UCASE(CustomerName), City FROM Customers;
--SQL Server
SELECT UPPER(CursoterName), City FROM Customers;
```
<br>

# SQL LCASET()
---
* field값을 소문자로 변환
```
-- General
SELECT LCASE(CustomerName), City FROM Customers;
-- SQL server
SELECT LOWER(CustomerName), City FROM CUstomers;
```
<br>

# SQL MID()
---
* text field로 부터 문자를 추출 할때 사용.
* start 는 1부터 시작
```
-- General
SELECT MID(City,1,4) AS ShortCity FROM Customers;
-- SQL Server
SELECT SUBSTRING(City,1,4) AS ShortCity FROM Customers;
```
<br>

# SQL LEN()
---
* text field의 길이는 반환.
```
SELECT CustomerName, LEN(Address) as LengthOfAddress FROM Customers;
```
<br>

# SQL ROUND()
---
* 소수점이하 값을 반올림 할때 사용
* 숫자에서 가까운 값으로 반올림 된다고 생각함. 어쨋든 많은 DBMS에서는 Bankers Rounding을 한다(짝수로 반올림을 한다)
* 11.3 -> 11이 되어야 한다고 생각하지만 Bankers Rounding 으로 12가 될수도 있다.
```
-- ProductName과 가격을 소수점이하 첫번째 자리에서 반올림해서 가져 옴.
SELECT ProductName, ROUND(Price,0) AS RoundedPrice FROM Products;
```
<br>

# SQL NOW()
---
* 시스템의 현재 날짜와 시간을 반환
```
-- ProductName과 가격, 시스템ㅇ시간을 PerDate이름으로 가져옴.
SELECT ProductName, Price, NOW() AS PerDate FROM Products;
```
<br>

# SQL FORMAT()
---
* 어떻게 화면에 display 될것인가를 정함 일반적으로 날짜의 형태
```
-- ProductName과 가격, 현재시간은 년(4)-월(2)-일(2) 로 가져 온다.
SELECT ProductName, Price, FORMAT(NOW(), 'YYYY-MM-DD') AS PerDate FROM Products
```