import sqlite3
import pandas as pd 

conn = sqlite3.connect('fake_employee.db')

def add_employee(job, state):
    ''' NOTE BOTH PERSONAL AND EMPLOYEE DETAILS MUST BE ADDED AT SAME TIME
    add a single entry to employee table.
    e_id integer PRIMARY KEY
    job text
    state text'''
    try:
        cur = conn.cursor()
        max_id = cur.execute('SELECT MAX(e_id) FROM employee')
        e_id = max_id.fetchone()[0] + 1
        query = 'INSERT INTO employee VALUES (?,?,?)'
        cur.execute(query, (e_id, job, state))
        conn.commit()
        return 'employee added'
    
    except:
        return 'failed to add employee'

def add_personal(name, dob=None, addr=None, email=None, country=None):
    ''' NOTE BOTH PERSONAL AND EMPLOYEE DETAILS MUST BE ADDED AT SAME TIME
    add a single entry to personal table.
    p_id integer PRIMARY KEY
    name text NOT NULL
    dob text
    address text
    email text
    country text
    '''
    try:
        cur = conn.cursor()
        max_id = cur.execute('SELECT MAX(e_id) FROM employee')
        p_id = max_id.fetchone()[0] + 1
        query = 'INSERT INTO personal VALUES (?,?,?,?,?,?)'
        cur = conn.cursor()
        cur.execute(query, (p_id, name, dob, addr, email, country))
        conn.commit()
        return 'person added'
    
    except :
        return "failed to add person"

def sql_query(query):
    return pd.read_sql_query(query, conn)

# SELECT all the table names FROM database WHERE it's type is a table
# Q1 = return all the table names from the database
query = '''
SELECT name 
FROM sqlite_master 
WHERE type = "table";
'''
print(sql_query(query))

# SELECT all columns, FROM personal table, LIMIT to 5 records
# Q2 = return the first 5 rows for each table in db
query = '''
SELECT * 
FROM personal 
LIMIT 5;
'''
print(sql_query(query))

# SELECT all columns, FROM employee table, LIMIT to 5 records
query = '''
SELECT * 
FROM employee 
LIMIT 5;
'''
print(sql_query(query))

# COUNT, SUM, AVG, MIN and MAX 
# WHERE, MULTIPLE CONDITIONS
# SELECT the COUNT of rows, FROM personal, WHERE country is equal to Sierra  Leone AND p_id is greater than 5000
# q3 = provide a count of people from a specified country with a specified id range
query = '''
SELECT COUNT(*) AS "People from Sierra Leone with personal ID > 5000"
FROM personal
WHERE country = "Sierra Leone" AND p_id > 5000;
'''
print(sql_query(query))

# SELECT MINimum id AS alias, SELECT MAXimum id AS alias, FROM employee table in db
# q4 = return the first and last id for the employees
query = '''
SELECT MIN(e_id) AS "First Employee ID", MAX(e_id) AS "Last Employee ID"
FROM employee;
'''
print(sql_query(query))

# SELECT job, SELECT COUNT of rows, FROM employee, GROUP BY the job title, ORDER BY frequency of job in descending order, LIMIT results to top 5
# q5 = return the top 5 most popular jobs from the data
query = '''
SELECT job AS "Job", COUNT(*) AS "Frequency"
FROM employee
GROUP BY job
ORDER BY COUNT(*) DESC
LIMIT 5;
'''
print(sql_query(query))

# SELECT job from employee, SELECT name from personal, FROM personal INNER JOIN empoloyee ON p_id and e_id, 
# ORDER BY personal id in DESCending order, LIMIT results to first 5
# q6 = match the names to the jobs by joining the tables
query = '''
SELECT personal.p_id AS "Personal ID", employee.job AS "Job", personal.name AS "Name"
FROM personal INNER JOIN employee
ON personal.p_id = employee.e_id
ORDER BY p_id DESC
LIMIT 5;
'''
print(sql_query(query))
