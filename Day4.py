from sqlalchemy import create_engine, text
import sqlite3

#Connect to database(creates a file name called company.db)
engine=create_engine("sqlite:///company.db",echo=True)

#Create table
with engine.begin() as conn:
    conn.execute(text("""
                      Create Table if not exists employees(
                      ID Integer Primary Key AutoIncrement,
                      Name Text Not Null,
                      Salary Real Not Null,
                      Department Text Not Null)
    """))
    print("Table created successfully")

#Clearing out table before inseritn values
with engine.begin() as conn:
    conn.execute(text("Delete from employees"))
    print("\nTable cleared!")

#Inserting values
with engine.begin() as conn:
    conn.execute(text("""Insert into employees
                      (name,salary,department) values(:name, :salary, :department)
                      """),[{"name":"John","salary":45000,"department":"HR"},
                            {"name":"Alicia","salary":72000,"department":"Tech"},
                            {"name":"Kane","salary":99000,"department":"Tech"},
                            {"name":"Maria","salary":64000,"department":"Tech"},
                            {"name":"Simon","salary":53000,"department":"HR"}]
                      )
    print("records inserted")

#Read all records
with engine.begin() as conn:
    result=conn.execute(text("Select * from employees"))
    print("\n---All Employees---")
    for row in result:
        print(row)

#Update and Delete operations
with engine.begin() as conn:
    conn.execute(text("""
Update employees set salary= :salary where name= :name"""),{"salary":87000,"name":"Kane"})

#Verify Update
with engine.begin() as conn:
    result=conn.execute(text("Select * from employees where name= :name"),{"name":"Kane"})
for row in result:
    print(row)

#Delete 
with engine.begin() as conn:
    conn.execute(text("Delete from employees where name= :name"),{"name": "Maria"})

#Verify delete
with engine.begin() as conn:
    result=conn.execute(text("Select * from employees where name= :name"),{"name":"Maria"})
for row in result:
    print(row)    
