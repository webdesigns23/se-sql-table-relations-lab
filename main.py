# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

# table = pd.read_sql("""SELECT * FROM sqlite_master""", conn)
# print(table)

# table = pd.read_sql("""SELECT * FROM customers""", conn)
# print(table.head())

# STEP 1
df_boston = pd.read_sql(""" 
SELECT firstName, lastName
FROM employees
JOIN offices
    USING(officeCode)
WHERE offices.city = "Boston"
""",conn)

# STEP 2
df_zero_emp = pd.read_sql(""" 
SELECT
    offices.officeCode, COUNT(employees.employeeNumber) AS number_employees
FROM offices
JOIN employees
    USING(officeCode)
GROUP BY officeCode
HAVING number_employees = 0
""",conn)

# STEP 3
df_employee = pd.read_sql(""" 
SELECT employees.firstName, employees.lastName, offices.city, offices.state
	FROM employees
	JOIN offices
	USING(officeCode)
ORDER BY employees.firstName, employees.lastName ASC
""", conn)

# STEP 4
df_contacts = pd.read_sql(""" 
SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
FROM customers AS c
	LEFT JOIN orders
	USING(customerNumber)
WHERE orders.customerNumber IS NULL
ORDER BY c.contactLastName ASC						  
""", conn)

# STEP 5
df_payment = pd.read_sql(""" 
SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate
FROM customers AS c
	JOIN payments AS p
	USING(customerNumber)
ORDER BY CAST(p.amount AS INTEGER) DESC
""",conn)

# STEP 6
df_credit = pd.read_sql(""" 
SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS num_of_customers
FROM employees AS e
JOIN customers AS c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber
HAVING AVG(c.creditLimit) > 90000
ORDER BY num_of_customers DESC
LIMIT 4
""",conn)

# STEP 7
df_product_sold = pd.read_sql(""" 
SELECT p.productName, COUNT(o.orderNumber) AS numorders, SUM(o.quantityOrdered) AS totalunits
FROM products AS p
JOIN orderdetails as o
USING(productCode)
GROUP BY productCode
ORDER BY totalunits DESC
""",conn)

# STEP 8
df_total_customers = pd.read_sql(""" 
SELECT p.productName, od.productCode, COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM products AS p
JOIN orderdetails AS od USING(productCode)
JOIN orders AS o USING(orderNumber)
GROUP BY productCode
ORDER BY numpurchasers DESC
""",conn)

# STEP 9
df_customers = pd.read_sql(""" 
SELECT o.officeCode, o.city, COUNT(DISTINCT c.customerNumber) AS n_customers
FROM offices AS o
JOIN employees AS e USING(officeCode)
JOIN customers AS c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY officeCode
""",conn)

# STEP 10
df_under_20 = pd.read_sql(""" 
SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, of.city, e.officeCode
FROM employees AS e
JOIN offices AS of USING(officeCode)
JOIN customers as c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders USING(customerNumber)
JOIN orderdetails USING(orderNumber)
JOIN products AS p USING(productCode)
WHERE p.productCode IN(					  						  
	SELECT p.productCode
	FROM products AS p
	JOIN orderdetails AS od USING(productCode)
	JOIN orders AS o USING(orderNumber) 
	GROUP BY p.productCode
	HAVING COUNT(DISTINCT o.customerNumber) <= 19
)
ORDER BY e.lastName
""",conn)
print(df_under_20)

conn.close()
