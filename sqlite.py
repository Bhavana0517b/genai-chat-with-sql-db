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
cursor.execute('''Insert Into STUDENT Values('John','Data Science','B', 100)''')
cursor.execute('''Insert Into STUDENT Values('Mukesh','Data Science','A', 86)''')
cursor.execute('''Insert Into STUDENT Values('Jacob','DEVOPS','A', 50)''')
cursor.execute('''Insert Into STUDENT Values('Dipesh','DEVOPS','A', 35)''')

##Display all the records
print("Te inserted records are")
data=cursor.execute('''select * from STUDENT''')
for row in data:
    print(row)

##commit your changes in the database
connection.commit()
connection.close()