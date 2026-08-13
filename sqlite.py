import sqlite3

##connect to sqlite
connection=sqlite3.connect("student.db")

##create a cursor obejct to insert record, create table
cursor=connection.cursor()

##create the table
table_info="""
create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25),
SECTION VARCHAR(25), MARKS INT)
"""

cursor.execute(table_info)

##insert some more records
cursor.execute('''Insert Into STUDENT Values('krish','Data Science','A', 90)''')
cursor.execute('''Insert Into STUDENT Values('Mukesh','Data Science','B', 100)''')
cursor.execute('''Insert Into STUDENT Values('Jacob','Data Analytics','B', 77)''')
cursor.execute('''Insert Into STUDENT Values('Karthik','Data Analytics','B', 95)''')
cursor.execute('''Insert Into STUDENT Values('Nirmal','GENAI','A', 99)''')
cursor.execute('''Insert Into STUDENT Values('Sunil','DBMS','B', 98)''')

##Display all the records
print("Te inserted records are")
data=cursor.execute('''select * from STUDENT''')
for row in data:
    print(row)

##commit your changes in the database
connection.commit()
connection.close()
