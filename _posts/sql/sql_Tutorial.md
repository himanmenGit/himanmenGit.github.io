# SQL(Structured Query Language) Tutorial
---
* 정보를 가공하고 잘 정리하기에 필수적인 요소는 Database이다.
* Database로 인해 회원가입, 게시판 등등을 만들 수 있다.
* Mysql, SQL server, Access, Oracle 등등 이런것들을 관계형 데이터 베이스(RDBMS)라고 함.
* 이러한 데이터베이스에 정보를 가져오고, 저장, 수정, 검색등을 하기 위한 공통의 언어가 SQL 이다.
* 여러 데이터베이스들이 있지만 기본적인것(SELECT, UPDATE, DELETE, INSERT, WHERE) 들은 표준을 따른다.
* RDBMS에서의 데이터는 테이블이라는 데이터베이스객체를 사용하여 저장된다.
<br>

# SQL Syntax
---
* ** Database Table **
각 테이블마다 이름이 존재 함.
columns(세로)[field]와 rows(가로)[record]
* ** SQL Statements **
데이터를 조작(등록, 삭제, 수정, 검색)하기 위한 SQL 문
>`SELECT * FROM Customers;`
* ** SQL 문은 대소문자를 구별하지 않는다. **
* ** SQL 문은 마지막에 `;` 을 적어 준다. **
* ** 가장 중요한 SQL문 일부 **
>
SELECT - 데이터를 가져 온다.
UPDATE - 데이터를 수정 한다.(기본구조를 유지 하고 데이터의 값만 수정)
DELETE - 데이터를 삭제 한다.
INSERT INTO - 데이터를 삽입 한다.
CREATE DATABASE - 데이터 베이스를 새로 만든다. (관리자용)
ALTER DATABASE - 데이터 베이스를 수정 한다.
CREATE TABLE - 테이블을 생성한다.
ALTER TABLE - 테이블을 수정한다.(필드의 구조를 바꾸거나 추가하는 것)
DROP TABLE - 테이블을 삭제 한다.
CREATE INDEX - 인덱스를 만든다.
DROP INDEX - 인덱스를 삭제 한다.
<br>

# SQL SELECT Statement
---
* result-set이라고하는 result table에 result가 저장 된다.
```
// Customers테이블의 CustomerName, City Field를 가져 온다.
SELECT CustomerName, City From Customers;
// Customers테이블의 모든 Field와 ROW를 가져 온다.
SElect * FROM Customers;
```
* 서버 언어를 이용하여 SQL로 불러온 데이터를 가공 할 수 있다.(PHP, ASP 등)
<br>

# SQL SELECT DISTINCT Statement
---
* 특정 필드에 대해 값이 겹칠수가 있는데, 이것을 유일한 값으로 구분하여 가져 올 수 있다.
```
// Customers테이블의 City Field를 가져 올떄 중복된 값을 하나로 합쳐서 가져 온다.
SELECT DISTINCT City FROM Customers;
```
<br>

# SQL WHERE Clause
---
* 데이터의 수많은 ROW중에서 원하는 조건에맞는 데이터만 추출 할 수 있다.
```
// country가 Mexico인 것만 가져 온다.
SELECT * FROM Customers WHERE country='Mexico';
```

* 텍스트 field일 경우 ''로 감싸야 한다. 숫자 field일 경우 그냥 들고 오면된다.
* 대부분의 데이터베이스 시스템에서는 ""도 허용 한다.
```
// CustomerID가 1인 경
SELECT * FROM Customers WHERE CustomerID=1;
```
* 연산자
	- `=` : 값이 같은 것을 가져 온다.
	- `<>` : 값이 같지 않은 것을 가져 온다. (다른 언어의 !=와 같다)
	- `>` : 값이 크면 가져 온다.
	- `<` : 값이 작으면 가져 온다.
	- `>=` : 값이 크거나 같으면 가져 온다.
	- `<=` : 값이 작거나 같으면 가져 온다.
	- `BETWEEN` : 값의 사이를 검색 할때.
	- `LIKE` : 패턴을 검색할때 사용.
	- `IN` : 2개이상의 가능한 값을 검색 할때.
<br>

#SQL AND & OR Operators
---
* 두개 이상의 조건이 주어 질 경우 AND & OR 연산자를 사용한다.
	- `AND` : 두개의 조건이 모두 참일때 가져 온다.
	- `OR` : 한개의 조건이라도 참이면 가져 온다.

* AND 연산자	
```
// Country가 Germany이면서 City가 Berlin인 경우
SELECT * FROM Customers WHERE Country='Germany' AND city='Berlin';
```
* OR 연산자
```
// City가 Berlin이거나 City가 Muchen인 경우
SELECT * FROM Customers WHERE City='Berlin' OR City='Muchen';
```

* NOT 연산자
```
// Country가 Germany가 아닌 경우
SELECT * FROM Customers WHERE NOT Country='Germany';
```

* Combining AND & OR
```
// City가 Berlin이거나 London 이면서 Conutry가 Germany인 경우
SELECT * FROM Customers WHERE Country='Germany' AND (City='Berlin' OR City='London');
```
```
// Country가 Germany가 아니며 Country가 USA도 아닌 경우
SELECT * FROM Customers WHERE NOT Country='Germany' AND NOT Country='USA';
```
<br>

# SQL ORDER BY Keyword
---
* 데이터 베이스를 어떤 순서로 가져 올 것인가 할때 사용.
* 결과를 가져 올때 Keyword를 기준으로 정렬 한다.(왼쪽 기준 우선)
* ASC가 default값이다.
```
// Country를 기준으로 정렬하여 가져 온다.(A-Z)
SELECT * FROM Customers OERDER BY Country;
```
```
// Countyer를 기준으로 한번 정렬을 하고 CustomerName으로 하위 정렬을 하여 가져 온다.
SELECT * FROM Customers OERDER BY Country, CustomerName;
```
```
// Country를 오름차순으로 한번 정렬을 하고 CustomerName으로 하위 정렬을 내림차순하여 가져 온다.
SELECT * FROM Customers ORDER BY Country ASC, CustomerName DESC;
```
<br>

# SQL NULL Values
---
* NULL값이 있는 필드는 값이 없는 필드 이다.
* NULL값은 0 과 공백과는 다르다.
* 비교 연산자로 NULL값을 확인할수 없다.
* `IS NULL` 연산자나 `IS NOT NULL`연산자로 확인 해야 한다.
```
// NULL값을 찾으려면 항상 IS NULL을 사용 하라.
// Persons 테이블에서 Address가 NULL인 경우의 LastName, FirstName, Address를 가져 온다.
SELECT LastName, FirstName, Address FROM Persons WHERE Address IS NULL;
```
```
// Persons테이블에서 Address가 NULL이 아닌경우의 LastName, FirstName, Address를 가져 온다.
SELECT LastName, FirstName, Address FROM Persons WHERE Address IN NOT NULL;
```
# SQL INSERT INTO Statement
---
* 테이블에 데이터를 추가저장 할때 사용.
* Primary Key는 AutoIncreament로 자동으로 Indexing이 된다.
* 두개의 구문이 있다. (column 이름을 지정하지 않는경우, column을 지정 하는 경우)
```
// 모든 field에 대해 값을 넣고 삽입한다.
INSERT INTO Customers (CutomerName, ContactName, Address, City, PostalCode, Country) VALUES ('Cardinal', 'Tom B. Erichen', 'Skagen 21', 'Stavagner', '4006', 'Norway');
```
* 특정 열에만 데이터를 삽입 할 수 있다. 넣지 않은 field에는 null값이 들어 간다.
```
// CustomerName, City, Country를 지정된 VALUES로 대입하여 삽입한다.
INSERT INTO Customers (CustomerName, City, Country) VALUES ('Cardinal', 'Stavanger', 'Norway')
```
<br>

# SQL UPDATE Statement
---
* 기존 데이터를 수정할때 사용.
* *** UPDATE문은 WHERE절을 사용하여 정확한 조건에 해당하는 ROW만 수정해야 한다. ***
* SET - 변경할 데이터들
* WHERE -변경하고자 하는 ROW들
```
// contactName이 Alfed Futterkiste라는 사람의 contactName을 'alfred Schmidt'로 City를 'Hamburg'로 바꾼다.
UPDATE Customers SET contactName='Alfred Schmidt', City='Hamburg' WHERE CustomerName='Alfeds Futterkiste';
```
* WHERE절을 빼면 모든 필드의 데이터가 수정된다.
<br>

# SQL DELETE Statement
---
* 테이블에 기록된 ROW를 삭제 할떄 사용 한다.
* *** DELETE문은 WHERE절을 사용하여 정확한 조건에 해당하는 ROW만 삭제 해야 한다 ***
* WHERE - DELETE하고자 하는 ROW들
```
// CustomerName이 'Alfreds Futterkiste' 이고 ContactName이 Maria Anders'인 ROW를 삭제 함.
DELETE FROM Customers WHERE CustomerName='Alfreds Futterkiste' AND ContactName = 'Maria Anders';
```
* WHERER절이 없이 DELETE를 할경우 해당 테이블의 모든 데이터를 삭제 한다.
```
// Customers테이블을 초기화 시킨다.
// WHERE절이 빠진 DELETE를 하는 것과 비슷
// 테이블을 DROP하고 새로 생성하는 것과 동일
TURNCATE table Customers; 
```
<br>

# SQL Injection
---
* 데이터 베이스를 파괴 할 수 있다.
* 악의적인 사용자가 SQL 구문을 활용해 데이터 베이스를 변조하여 파괴 하는 것.
* WHERE절을 이용한 `or 1=1` 등의 구문으로 항상 TRUE를 리턴하게 하는 방법.
* SQL Injecton은 ""=""이 항상 TRUE인것을 기본으로 한다.
* DROP 같은 민감한 SQL문에 대해 아무나 할수 없게 권한을 부여 한다.
* Injection을 막기 위한방법으로 SQL Parameters를 추가 한다.

```
txtName = getRequestString('CustomerName');
txtAdd  = getRequestString('Address');
txtCity = getRequestString('CIty');
txtSQL  = "INSERT INTO Customers (CUstomerName, Address, City) Values(@0, @1, @2)";
// db.Execute(SQL, @0, @1, @2)
db.Execute(txtSQL, txtName, txtAdd, txtCity)
```
<br>

# SQL SELECT TOP
---
* DB부터 데이터를 가져 올 때 가져올 수를 지정할때 사용.
* 테이블이 거대하거나 데이터가 많을 때 사용.
* 숫자로 지정하거나 %로 지정해서 가져올수 있지만. 성능에 영향을 준다.
* 모든 RDBMS가 지원하는 것은 아니다.
* DB의 종류마다 사용하는 문법이 다를 수 있다.
* SELECT TO(MS SQL) | LIMIT(MY SQL) | ROWNUM(Oracle)
```
// default ID 순으로
// Customers 테이블에서 2개의 데이터를 가져 온다. 
SELECT TOP 2 * FROM Customers;
SELECT * FROM Customers LIMIT 5;
SELECT * FROM Customers WHERE ROWNUM <= 3;
```
```
// Customers 테이블에서 50%의 데이터를 가져 온다.
SELECT TOP 50 PERCENT * FROM Customers;
```
```
// Country가 Gernamy인것중 3개를 가져 온다.
SELECT TOP 3 * FROM Customers WHERE Country='Germany';
SELECT * FROM Customers WHERE Country='Germany' LIMIT 3;
SELECT * FROM Customers WHERE Country='Germany' AND ROWNUM <= 3;
```
<br>

# SQL Min and Max
---
* `Min()`는 선택된 컬럼에서 가장 작은 값을 가져 옴.
* `Max()`는 선택된 컬럼에서 가장 큰 값을 가져옴.
```
// Products 테이블에서 Price컬럼의 가장 작은 값을 SmallestPrice라는 이름으로 바꿔서 가져 온다.
SELECT MIN(Price) AS SmallestPrice FROM Products;
```
```
// Products 테이블에서 Price컬럼의 가장 큰 값을 LargestPrice라는 이름으로 바꿔서 가져 온다.
SELECT MAX(Price) AS LargestPrice FROM Products;
```
<br>

# SQL COUNT(), AVG(), and SUM() Functions
---
* `COUNT()`는 지정된 기준과 일치하는 ROW수를 반환한다.
* `AVG()`는 숫자 열의 평균값을 반환한다.
* `SUM()`은 숫자 열의 총 합계를 반환한다.
```
// Products테이블에서 총 ROW의 갯수를 반환.
SELECT COUNT(ProductID) FROM Products;
```
```
// Products테이블에서 Price컬럼의 평균값을 반환.
SELECT AVG(Price) FROM Products;
```
```
// OrderDetails테이블의 Quantity컬럼의 합계를 반환.
SELECT SUM(Quantity) FROM OrderDetails;
```
<br>

# SQL LIKE Operator
---
* WHERE 절에서 사용하며, 컬럼의 패턴(형태)를 지정할때 사용.
```
// 도시명이 s로 시작하는 도시의 ROW를 반환한다.
SELECT * FROM Customers WHERE City LIKE 's%';
```
```
// 도시명이 s로 끝나는 도시의 ROW를 반환한다.
SELECT * FROM Customers WHERE City LIKE '%s';
```
```
// Country가 land를 포함하는 것을 반환
SELECT * FROM Customer WHERE Country LIKE '%land%';
```
```
// CustomerName의 두번째 글자가 r인 ROW를 반환
SELECT * FROM Customers WHERE CustomerName LIKE '_r%'
```
```
// CustomerName이 a로 시작하고 3글자 이상인 ROW를 반환
SELECT * FROM Customers WHERE CustomerName LIKE 'a_%_%';
```
```
// CusotmerName이 a로 시작하고 o로 끝나는 ROW를 반환
SELECT * FROM Customers WHERE CustomerName LIKE 'a%o';
```
```
// Country가 land를 포함하지 않는 것을 반환
SELECT * FROM Customers WHERE Country NOT LIKE '%land%';
```
<br>

# SQL Wildcards
---
* WHERE 이하의 패턴에서 SQL LIKE operator와 사용
* 테이블의 데이터를 검색하는데 사용된다.
* `%` - 문자를 0또는 하나이상을 대체할때 사용 함.
* `_` - 문자를 오직 1개만 대체 할때 사용 함.
* `[charlist]` - 매치되는 집합 또는 범위를 지정할 때 사용.
* `[^charlist]or[!charlist]` - 매치되지 않는 집합 또는 범위를 지정할 때 사용.
```
// City가 ber로 시작하고 뒤에 무엇이 와도 상관없는 ROW를 반환 
SELECT * FROM Customers WHERE City LIKE 'ber%';
```
```
// City가 er를 포함하고 앞뒤 무엇이 와도 상관없는 ROW를 반환
SELECT * FROM Customers WHERE City LIKE '%es%';
```
```
// City가 임의문자1개+erlin으로 끝나는 ROW를 반환 
SELECT * FROM Customers WHERE City LIKE '_erlin';
```
```
City가 L+임의문자1개+n+임의문자1개+on 인 ROW를 반환
SELECT * FROM Customers WHERE City LIKE 'L_n_on';
```
```
// City가 b,s,p중 하나로 시작하고 뒤에 무엇이와도 상관없는 ROW를 반환
SELECT * FROM Customers WHERE City LIKE '[bsp]%'
```
```
// City가 a,b,c중 하나로 시작하고 뒤에 무엇이 와도 상관없는 ROW를 반환
SELECT * FROM Customers WHERE City LIKE '[a-c]%'
```
```
// City가 b,s,p로 시작하지 않고 뒤에 무엇이 와도 상관없는 ROW를 반환
SELECT * FROM Customers WHERE City '[!bsp]%';
or
SELECT * FROM Customers WHERE City NOT LIKE '[bsp]%';
```
<br>

# SQL IN Operator
---
* WHERE절에서 다중 조건을 지정하기 위해 사용
```
// Country가 Germany, France, UK면 ROW를 반환.
SELECT * FROM Customers WHERE Country IN ('Germany', 'France', 'UK');
```
```
// Country가 Germany, France, UK가 아니면 ROW를 반환.
SELECT * FROM Customers WHERE Country NOT IN ('Germany', 'France', 'UK);
```
```
// Customers 테이블에서 Country가 Suplliers테이블의 Country와 같은 ROW를 반환.
SELECT * FROM Customers WHERE Country IN (SELECT Country FROM Suppliers);
```
<br>

# SQL BETWEEN Operator
---
* 주어진 범위 사이의 값을 선택 할때 사용.
* 숫자, 문자, 날짜 등을 선택하여 범위설정 가능.

```
// Price가 10과 20사이인 ROW를 반환. (10, 20 포함)
SELECT * FROM Products WHERE Price BETWEEN 10 AND 20;
```
```
// Price가 10과 20 사이가 아닌 ROW를 반환. (<=9 AND 21>=)
SELECT * FROM Prdocuts WHERE Peice NOT BETWEEN 10 AND 20;
```
```
// Price가 10과 20사이이면서 CategoryID가 1,2,3 이 아닌 ROW 반환
SELECT * FROM Products WHERE (Price BETWEEN 10 AND 20) AND NOT CategoryID IN (1, 2, 3);
```
```
// ProductName이 'Carnarvon Tigers'와 'Mozzarella di Giovanni' 사이인 ROW를 ProductName을 기준으로 반환. (알파벳순)
SELECT * FROM Products WHERE ProductName BETWEEN 'Carnarvon Tigers' AND 'Mozzarella di Giovanni' ORDER BY ProductName;
```
```
// ProductName이 'Carnarvon Tigers'와 'Mozzarellas di Giovanni' 사이가 아닌 ROW를 ProductName을 기준으로 반환. (알파벳순)
SELECT * FROM Products WHERE ProductName NOT BETWEEN 'Carnarvon Tigers' AND 'Mozzarella di Giovanni' ORDER BY ProductName;
```
```
// OerderDate가 1996년7월4일과 1996년7월9일 사이인 ROW를 반환 (#으로 감싸준다.)
SELECT * FROM Orders WHERE OrderDate BETWEEN #07/04/1996# AND #07/09/1996#;
```

# SQL Aliases
---
* 테이블이름이나 컬럼이름을 별칭으로 대체해서 가져 올때 사용.
* 기본적으로 긴 테이블명, 긴 컬럼명을 간단하게 바꿔서 이용할때 사용.
* 가독성을 위해 사용.
* 두개이상의 테이블을 조합해서 가져 올떄 사용
* 컬럼 이름 바꾸
```
// Customers 테이블에서 CustomerID는 ID라는 이름으로, CustomerName은 Customer로 ROW를 반환.
SELECT CustomerID as ID, CustomerName as Customer FORM Customers;
```
```
// Customers테이블에서 CustomerName은 Customer로 ContactName은 Contact Person으로 바꿔서 ROW를 반환 ([띄어쓰기를 포함하기 위함.])
SELECT CustomerName AS Customer, ContactName AS [Contact Person] FROM Customers;
```
```
// Address와 PostalCode, City, Country를 Address로 묶어서 ROW를 반환
SELECT CustomerName, Address + ', ' + PostalCode + ', ' + City + ', ' + Country AS Address;
```
or
```
SELECT CustomerName, CONCAT(Address,', ',PostalCode,', ',City,', ',Country) AS Address FROM Customers;
```
* 테이블 이름 바꾸기
```
// Customers테이블은 c로 Oerders테이블은 o로 바꾸어 Customers테이블의 CustomerName이 'Around the Horn' 이고 Customers테이블의 CustomerID가 OrderDate의 CustomerID와 같으면 Orders의 OrderID, OrderDate와 Customers테이블의 CustomerName을 가져옴.
SELECT o.OrderID, o.OrderDate, c.CustomerName 
FROM Custoers AS c, Orders AS o 
WHERE c.CustomerName='Around the Horn' AND c.CustoerID=o.CustomerID;
```
or - 이 구문은 위와 같지만 별칭이 없다.
```
SELECT Orders.OrderID, Orders.OrderDate, Customers.CustomerName 
FROM Customers, Orders 
WHERE Customers.CustomerName="Arond the Horn" AND Customers.CustomerID=Orders.CustoerID;
```
* Aliases를 사용 하는경우
	* 쿼리가 두개 이상의 테이블에 연결 되어 있을때.
	* 쿼리에서 함수를 사용 할때.
	* 컬럼이름이 매우 길거나 읽을수 없을때.
	* 두개 이상의 컬럼을 결합하여 가져 올떄.
<br>

# SQL Joins
---
* 두개 이상의 테이블에서 데이터를 가져와 결합하는데 사용.
* 결합하는 테이블에 공통 컬럼이 존재 할때 사용 할수 있다.
* 일반적인 JOIN 인 SQL INNER JOIN(Simple join)이 있다. 이는 WHERE절이 일치 하는 두 개 이상의 테이블에서 데이터를 가져 온다.
```
// Orders과 INNER JOIN 한 Custommers에서 Orders테이블의 OrderID, OrderDate, Customers테이블의 CustomerName을 Orders테이블의 CustomerID와 Customers의 CustomerID가 같은 ROW를 반환.
SELECT Orders.OrderID, Customers.CustomerName, Orders.OrderDate FROM Orders INNER JOIN Customers ON Orders.CUstomerID=Customers.CustoerID
```
* SQL JOIN의 유형
	* (INNER) JOIN : 두 테이블에서 값이 일치하는 ROW를 반환
	* LEFT (OUTER) JOIN : 왼쪽 테이블에서 모든 ROW를 반환하고, 오른쪽 테이블에서는 일치하는 ROW만 반환
	* RIGHT (OUTER) JOIN : 오른쪽 테이블에서 모든 ROW를 반환하고, 왼쪽 테이블에서는 일치하는 ROW만 반환
	* FULL (OUTER) JOIN : 왼쪽 또는 오른쪽 테이블에 일치하는 항목이 있으면 모든 ROW를 반환
<br>

# SQL INNER JOIN
---
* 두개의 테이블에서 값이 일치하는 ROW를 반환
* `SELECT * FROM table1 INNER JOIN table2` 와 `SELECT * FROM table1 JOIN table2`는 같다

```
// Order와 Customers를 Join함. Orders의 CustomerID와 Customers의 CustomerID가 같은 Customers의 CustomerName과 Orders의 OrderID를 가져 옴.
SELECT Orders.OrderID, Customers.CustomerName FROM Orders INNER JOIN Customers ON Orders.CustomerID=Customers.CustomerID;
```
* 세개의 테이블 JOIN
```
// Orders와 Customers, Shippers를 Join함.
// Orders와Customers의 CustomerID와 같은 JOIN테이블과 Shippers를 JOIN하여 Orders와 SHippers의 ShipperID가 같은 ROW를 반환.
SELECT Orders.OrderID, Customers.CustomerName, Shippers.ShipperName 
FROM ((Orders 
INNER JOIN Customers ON Orders.CustomerID=Customers.CustomerID)
INNER JOIN Shippers ON Orders.ShipperID=Shippers.ShipperID);
```
<br>

# SQL LEFT JOIN
---
* OUTER JOIN으로 분류 된다.
* LEFT 테이블에 있는 모든 ROW는 다 가지고 오고, RIGHT 테이블에서는 일치하는 ROW만 반환.
* RIGHT 테이블에 일치하는 데이터가 없어도 LEFT 테이블에 대한 데이터는 가져 온다.
```
// Customers의 CustomerName은 모두 들고 오고 Orders와 Customers의 CustomerID같은 경우의 OrderID를 가져와서 합친다. 
// 이때 Customers에서 가져온 CustomerName들은 OrderID가 없으므로 null을 넣는다.
// Customers의 CustomerName기준으로 가져 온다.
SELECT Customers.CustomerName, Orders.OrderID FROM Customers
LEFT JOIN Orders ON Customers.CustomerID=Orders.CustomerID
ORDER BY Customers.CustomerName;
```
<br>

# SQL Right JOIN
---
* RIGHT 테이블에 있는 모든 ROW는 다 가져 오고, LEFT 테이블에서는 일치하는 ROW만 반환.
* LEFT 테이블에 일치하는 데이터가 없어도 RIGHT 테이블에 대한 데이터는 가져 온다.
* LEFT JOIN과 반대
```
// Employees의 LastName과 FirstName은 모두 가져오고 Orders와 Employees의 EmployeeID가 같은 ROW의 OrderID를 가져와서 합친다.
// 이때 Empolyees에서 가져온 ROW에는 OrderID가 없으므로 null 처리
// Orders의 OrderID를 기준으로 가져 온다(오름차순)
SELECT Orders.OrderID, Empolyees.LastName, Employees.FirstName FROM Orders
RIGHT JOIN Employees ON Orders.EmployeeID=Employees.EmployeeID
ORDER BY Orders.OrderID:
```
<br>

# SQL FULL OUTER JOIN keyword
---
* LEFT 테이블과 RIGHT테이블을 모두 가져 오면서 조건에 맞는 것을 합쳐서 가져 온다.
```
// Customers와 Orders의 CustomerID가 같은 것들 모두와 같지 않은 것들에 CustomerName과 OrderID를 CustomerName을 기준으로 가져 온다.
SELECT Customers.CustomerName, Orders.OrderID FROM Customers
FULL OUTER JOIN Orders Customers.CustomerID=Orders.CustomerID
ORDER BY Customers.CustomerName;
```
* 조건이 일치 하지 않는 행도 모두 표시 된다.
<br>

# SQL SELF JOIN
---
* 자신 테이블에 조인을 함.
```
// Customers의 CustomerID가 같지 않고 City가 같은 ROW들을 City의 오름차순으로 CustomerName1, CustomerName2로 Alias하여 City와 같이 가져 온다.
SELECT A.CustomerName AS CustomerName1, B.CustomerName AS CustomerName2, A.City
FROM Customers A, Customers B
WHERE A.CustomerID <> B.CustomerID
AND A.City = B.City
ORDER BY A.City;
```
<br>

# SQL UNION Operator
---
* 두개이상의 SELECT 구문에 의해서 가져온 결과를 조합한다.
* JOIN과는 다르게 각자 SELECT 구문을 통해 데이터를 가져 온다.
* 그래서 각각 가져 오는 columns의 수가 같아야 한다
* 또한 각각의 columns이 dateType이 유사한 데이터 타입을 가져야 한다.
* 역시 각각의 columns은 같은 순서로 있어야 한다.
* 기본적으로 distinct를 가져 온다.(중복제거)
* UNION ALL을 사용할 경우 distinct를 사용 하지 않는다.(중복제거안함)
```
// Customers에서 City를 Suppliers에서 City를 City로 정렬하여 `distinct()`(중복제거) 하여 가져 온다.
SELECT City FROM Customers
UNION
SELECT City FROM Suppliers
ORDER BY City;
```
```
// Customers에서 City를 Suppliers에서 City를 City로 정렬하여 가져 온다.
SELECT City FROM Customers
UNION ALL
SELECT City FROM Suppliers
ORDER BY City;
```
```
// Customers에서 City를 Country가 Germany인것만
// Suppliers에서 City를 Country가 Germany인것만 가져와서 City로 정렬하여 `distinct()`(중복제거)하여 가져 온다.
SELECT City, Country FROM Customers
WHERE Country='Germany'
UNION
SELECT City Country FROM Suppliers
WHERE Country='Germany'
ORDER BY City;
```
```
// Customers에서 City를 Country가 Germany인것만
// Suppliers에서 City를 Country가 Germany인것만 가져와서 City로 정렬하여 가져 온다.
SELECT City, Country FROM Customers
WHERE Country='Germany'
UNION ALL
SELECT city Country FROM Suppliers
WHERE Country='Germany'
ORDER BY City;
```
```
// Customers에서 가져온것은 Type컬럼에 Customer라는문자열을 Suppliers에서 가져온것은 Sipplier라는 문자열을 넣고
// ContactName, City, Country를 가져 온다.
SELECT 'Customer' As Type, ContactName, City, Country FROM Customers 
UNION
SELECT 'Supplier', ContactName, City, Country FROM Suppliers
```
<br>

# SQL GROUP BY Statement
---
* COUNT, MAX, MIN, SUM, AVG와 같이 사용해 결과들을 하나이상의 columns로 그룹화 한다.
```
// Customers의 CustomerID를 Country별로 세어 반환 한다,.
SELECT COUNT(CustomerID), Country FROM Customers GROUP BY Country;
```
```
// Customers의 CustomerID를 Country별로 세어 CustomerID가 많은 순으로 반환 한다.
SELECT COUNT(CustomerID), Country FROM Customers GROUP BY Country ORDER BY COUNT(CustomerID) DESC;
```
* GROUP BY With Join
```
// Shippers와 Orders에서 ShipperID가 같은 것을 세어 ShipperName으로 그룹화 하여 반환.
SELECT Shippers.ShipperName, COUNT(Orders.OrderID) AS NumberOfOrders FROM Orders
LEFT JOIN Shippers ON Orders.ShipperID=Shippers.SHipperID
GROUP BY ShipperName;
```
<br>

# SQL HAVING Clause
---
* 집계함수와 같이 사용 되며, GROUP를 이용하는 곳에서 사용한다.
* 집계 함수가 WHERE절 처럼 사용 할 수 없어서 추가된 구문
```
// Cusotmers테이블의 CustomerID를 카운팅 하여 Country기준으로 가져 오는데 CustomerID의 카운팅 수가 5개 이상인것만 가져 온다.
SELECT COUNT(CustomerID), Country FROM Customers GROUP BY Country HAVING COUNT(CustomerID) > 5;
```
```
// Cusotmers테이블의 CustomerID를 카운팅 하여 Country기준으로 가져 오는데 CustomerID의 카운팅 수가 5개 이상인것만 가져 온다.
// CustomerID의 카운팅이 많은 순으로 정렬해서 가져 온다.
SELECT COUNT(CustomerID), Country FROM Customers GROUP BY Country HAVING COUNT(CustomerID) > 5 ORDER BY COUNT(CustomerID) DESC;
```
```
// Orders와 Employees의 EmployeeID가 같은것중 LastName으로 그룹화 하여 
// OrderID가 10개이상이면 해당 LastName과 OrderID를 카운트 하여 가져 온다.
SELECT Employees.LastName, COUNT(Orders.OrderID) AS NumberOfOrders 
FROM (Orders INNER JOIN Employees
ON Orders.EmployeeID=Employees.EmployeeID)
GROUP BY LastName
HAVING COUNT(Orders.OrderID) > 10;
```
```
// Orders와 Employees의 EmployeeID가 같은것중 LastName이 'Davolio'거나 'Fuller'인 ROW를 LastName으로 그룹화 하여
// OrderID가 25개 이상이면 해당 LastName과 OrderID를 카운트 하여 가져 온다.
SELECT Employees.LastName, COUNT(Orders.OrderID) AS NumberOfOrders
FROM Orders INNER JOIN Employees
ON Orders.EmployeeID=Employees.EmployeeID
WHERE LastName='Davolio' OR LastName='Fuller'
GTOUP BY LastName
HAVING COUNT(Orders.OrderID) > 25;
```
<br>

# SQL EXISTS Operator
---
* 하위 쿼리에 레코드가 있는지 테스트 하는데 쓰인다.
* 하위 쿼리가 하나 이상의 레코드를 반환하면 TRUE를 반환한다.
```
// Products의 ProductsName을 SupplierId가 Suppliers.supplierId 같고 Price가 20보다 작을때 반환하는 값이 있으면
// Supplires의 SupplierName을 반환한다.
SELECT SupplierName FROM Suppliers 
WHERE EXISTS (SELECT ProductsName FROM Products WHERE SupplierId=Suppliers.supplierId AND Price < 20);
```
```
// Products의 ProductsName을 SupplierId가 Suppliers.supplierId 같고 Price가 22일때 반환하는 값이 있으면
// Supplires의 SupplierName을 반환한다.
SELECT SupplierName FROM Suppliers
WHERE EXISTS (SELECT ProductName FROM Products WHERE SupplierId=Suppliers.supplierId AND Price = 22);
```
<br>

# SQL ANY and ALL Operator
---
* ANY와 ALL연산자는 WHERE절 또는 HAVING절과 함께 사용 된다.
* ANY연산자는 하위 쿼리 값 중 하나가 조건을 충족하면 TRUE를 반환.
* ALL연산자는 모든 하위 쿼리 값이 조건을 충족하면 TRUE를 반환.
* 연산자는 표준 비교 연산자이여야 한다.
```
// OrderDetail에서 Quantity가 10인경우의 반환되는 ProductID중 ProductID와 같은것이 있으면 Products의 ProductName을 반환.
SELECT ProductName FROM Products
WHERE ProductID=ANY(SELECT ProductID FROM OrderDetail WHERE Quantity=10);
```
```
// OrderDetail에서 Quantity가 99보다 큰경우의 반환되는 ProductID중 ProductID와 같은것이 있으면 Products에서 ProductName을 반환한다.
SELECT ProductName FROM Products
WHERE ProductID=ANY(SELECT ProductID FROM OrderDetail WHERE Quantity>99);
```
```
SELECT ProductName From Products
// OrderDetail에서 Quantity가 10인 경우의 반환되는 ProductID들이 ProductID와 모두 같으면 Products의 ProductName을 반환
WHERE ProductID = ALL(SELECT ProductID FROM OrderDetail WHERE Quantity=10);
```
<br>

# SQL SELECT INTO Statement
---
* 한 테이블의 데이터를 새로운 테이블로 복사 한다.
* AS절을 사용하여 이름을 바꿀수 있다.

```
// Customers테이블의 모든 데이터를 CustomersBackup2018테이블로 복사 한다.
SELECT * INTO CustomersBackup2018 FROM Customers;
```
```
// IN 절을 사용하여 다른 데이터베이스에 테이블을 복사 한다.
SELECT * INTO CustomersBackup2018 IN 'Backup.mdb' FROM Customers;
```
```
// CustomerName, ContactName 컬럼만 CustomerBackup2018 테이블로 복사 한다.
SELECT CustomerName, ContactName INTO CustomersBackup2018 FROM Customers;
```
```
// Country가 Getmany인것만 가져와서 CustomerGermany테이블로 모두 복사 한다.
SELECT * INTO CustomersGermany FROM Customers WHERE Country = 'Germany';
```
```
// Customers와 Orders를 LEFT JOIN 하여 
// Customers테이블과 CustomerID가 같은것에
// CustomerName, OrderID를 CustomerOrderBackup2018테이블로 복사 한다.
SELECT Customer.CustomerName, Orders.OrderID
INTO CustomerOrderBackup2018
FROM Customers
LEFT JOIN Orders ON Customers.CustomerID=Orders.CustomerID;
```
```
// 무적 부정 WHERE절을 사용하여 oldtable의 스키마를 가진 newtable을 생성할수 있다.
SELECT * INTO newtable FROM oldtable WHERE 1 = 0;
```
<br>

# SQL INSERT INTO SELECT Statement
---
* 테이블의 데이터를 복사하여 다른 테이블에 복사 합니다.
* 소스 테이블과 타겟 테이블의 데이터 유형이 동일 해야 한다.
* 타겟 테이블의 기존 데이터에는 영향이 없다.

```
// Suppliers테이블에서 SupplierName, City, Country를 가져와
// Customers테이블의 CustomerName, City, Country에 삽입한다.
INSERT INTO Customers (CustomerName, City, Country)
SELECT SupplierName, City, Country FROM Suppliers;
```
```
// Suppliers테이블에서 SupplierName, Address, City, postalCode, Country를 가져와
// Customers테이블의 CustomerName, , Address, City, postalCode, Country에 삽입한다.
// 모든 columns

INSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country)
SELECT SupplierName, ContactName, Address, City, PostalCode, Country FROM Suppliers;
```
```
// Suppliers의 Country가 Germany인 ROW에서만 SupplierName, City, Country를 가져와
// Customers테이블의 CustomerName, City, Country에 삽입한다.
INSERT INTO Customers (CustomerName, City, Country)
SELECT SupplierName, City, Country FROM Suppliers
WHERE Country='Germany';
```
<br>

# SQL NULL Funtions
---
* null에 연산자를 사용 할 수 없다.
* 이 함수들은 null이 있을경우 특정 값으로 대체하는 기능을 한다.
* MySql
```
// UnitPrice * (UnitsInStock + UnitsOnOrder(가 null이면 0으로 대체))
SELECT ProductName, UnitPrice * (UnitsInStock + IFNULL(UnitsOnOrder, 0))
FROM Products;
```
or
```
// UnitPrice * (UnitsInStock + UnitsOnOrder(가 null이면 0으로 대체))
SELECT ProductName, UnitPrice * (UnitsInStock + COALESCE(UnitsOnOrder, 0))
FROM Products;
```
* SQL Server
```
// UnitPrice * (UnitsInStock + UnitsOnOrder(가 null이면 0으로 대체))
SELECT ProductName, UnitPrice * (UnitsInStock + ISNULL(UnitsOnOrder, 0))
FROM Products;
```
* MS Access
```
// UnitPrice * (UnitsInStock + UnitsOnOrder가 Null이면 True를 반환 (0), 아니면 False를 반환 UnitsOnOrder
// IIF(boolean_expression, true_value, false_value)
SELECT ProductName, UnitPrice * (UnitsInStock + IIF(IsNull(UnitsOnOrder), 0, UnitsOnOrder))
FROM Products;
```
* Oracle
```
// UnitPrice * (UnitsInStock + UnitsOnOrder(가 null이면 0으로 대체))
SELECT ProductName, UnitPrice * (UnitsInStock + NVL(UnitsOnOrder, 0))
```
<br>

# SQL Comments
---
* 주석
```
--Select all:
SELECT * FROM Customers;
```
```
SELECT * FROM Customers; -- WHERE City='Berlin';
```
```
--SELECT * FROM Customers;
SELECT * FROM Products;
```
```
/*Select all the columns
of all the records
in the Customers table:*/
SELECT * FROM Customers; 
```
```
/*SELECT * FROM Customers;
SELECT * FROM Products;
SELECT * FROM Orders;
SELECT * FROM Categories;*/
SELECT * FROM Suppliers;
```
```
SELECT CustomerName, /*City,*/ Country FROM Customers;
```
```
SELECT * FROM Customers WHERE (CustomerName LIKE 'L%'
OR CustomerName LIKE 'R%' /*OR CustomerName LIKE 'S%'
OR CustomerName LIKE 'T%'*/ OR CustomerName LIKE 'W%')
AND Country='USA'
ORDER BY CustomerName;
```
<br>