from sqlalchemy import create_engine, text
import pandas as pd

#Database Setup
engine=create_engine("sqlite:///employee_mgmt.db", echo=False)

def create_table():
    with engine.begin() as conn:
        conn.execute(text("""Create table if not exists employees(
                          ID Integer Primary Key Not Null,
                          name Text not null,
                          salary real not null,
                          department Text not null)"""))
print("Database ready!")
create_table()

#Inserting values into table
# def add_employee(name,salary,department):
#     with engine.begin() as conn:
#         conn.execute(text("""
# Insert into employees(name,salary,department) values(:name,:salary,:department)
#                           """),{"name":name,"salary":salary,"department":department})
#         print(f"Employee {name} added successfully!")
# add_employee("Jenny",48000,"HR")
# add_employee("Ryan",85000,"Tech")
# add_employee("Connor",52000,"HR")
# add_employee("Rita",67000,"Tech")
# add_employee("Ivan",73000,"Tech")

#Read all employees
def read_emp():
    with engine.begin() as conn:
        result=conn.execute(text("Select * from employees"))
        df=pd.DataFrame(result.fetchall(),columns=result.keys())
    print("\n----All Employees----")
    print(df)
    return df
read_emp()

#Clearing out the table
# def clear_table():
#     with engine.begin() as conn:
#         conn.execute(text("Delete from employees"))
#     print("Table cleared !")
# clear_table()

#Adding update and delete functions
def update_salary(name,new_salary):
    with engine.begin() as conn:
        conn.execute(text("""
        Update employees set salary= :salary where name=:name"""),
        {"salary":new_salary,"name":name})
    print(f"{name}'s new updated salary is {new_salary}")

#Delete record
def delete_emp(name):
    with engine.begin() as conn:
        conn.execute(text("Delete from employees where name=:name"),{"name":name})
    print(f"{name} is deleted from table!")


update_salary("Jenny",55000)
delete_emp("Rita")

read_emp()

#Analytics department summary
def department_summary():
    df=read_emp()
    summary=df.groupby("department").agg(
        Total_Employees=("name","count"),
        Average_Salary=("salary","mean"),
        Max_Salary=("salary","max"),
        Min_Salary=("salary","min")
    ).reset_index()
    print(summary)
    return summary
department_summary()
