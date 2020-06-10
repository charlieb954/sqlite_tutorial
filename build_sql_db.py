import sqlite3
from faker import Faker
import pandas as pd 

# when you connect to a db that doesn't exist, it creases a new db for you
# sqlite3.connect(':memory:') will create a db in memory
conn = sqlite3.connect('fake_employee.db')

curs = conn.cursor()

query = '''
CREATE TABLE IF NOT EXISTS personal (
    p_id integer PRIMARY KEY,
    name text NOT NULL,
    dob text,
    address text,
    email text,
    country text
);
'''
curs.execute(query)

query = '''
CREATE TABLE IF NOT EXISTS employee (
    e_id integer PRIMARY KEY,
    job text NOT NULL,
    state text
);
'''
curs.execute(query)

conn.commit()

# create instance of faker
fake = Faker()

personal_list = []
employee_list = []
for i in range(0, 10000):
    # personal table
    name = fake.name()
    dob = fake.date_of_birth()
    addr = fake.address()
    email = fake.email()
    country = fake.country()
    personal_list.append((i, name, dob, addr, email, country))
    
    # employee table
    job = fake.job()
    state = fake.state()
    employee_list.append((i, job, state))

curs.executemany('INSERT INTO personal VALUES (?,?,?,?,?,?)', personal_list)
curs.executemany('INSERT INTO employee VALUES (?,?,?)', employee_list)

conn.commit()

conn.close()