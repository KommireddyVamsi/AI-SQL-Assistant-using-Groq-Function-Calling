import sqlite3

conn = sqlite3.connect("employees.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE employees (
    empid INTEGER,
    name TEXT,
    department TEXT
)
""")

cursor.execute("""
INSERT INTO employees VALUES
(1001,'Vamsi','Security')
""")

cursor.execute("""
INSERT INTO employees VALUES
(1002,'Ravi','HR')
""")

conn.commit()

print("Database Created")

conn.close()