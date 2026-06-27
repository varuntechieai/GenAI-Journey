from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine
from app.models import Employee,EmployeeUpdate
import pandas as pd

router=APIRouter()

#Get all employees
@router.get("/employees")
def get_emp():
    with engine.begin() as conn:
        result=conn.execute(text("Select * from employees"))
        df=pd.DataFrame(result.fetchall(),columns=result.keys())
    return df.to_dict(orient="records")

#Post - add single employee
@router.post("/employees")
def add_emp(emp: Employee):
    with engine.begin() as conn:
        conn.execute(text("""Insert into employees(name,salary,department) values(
                          :name,:salary,:department)"""),{"name":emp.name,"salary":emp.salary,"department":emp.department})
    return{"message":f"{emp.name} added successfully !"}

#Post - add bulk employees
@router.post("/employees/bulk")
def add_emp_bulk(emps:list[Employee]):
    with engine.begin() as conn:
        for emp in emps:
            conn.execute(text("""Insert into employees(name,salary,department) values(
                          :name,:salary,:department)"""),{"name":emp.name,"salary":emp.salary,"department":emp.department})
    return{"message":f"{len(emps)} has been added successfully !"}

#Put - Update salary
@router.put("/employees/{name}")
def update_emp(name: str,emp:EmployeeUpdate):
    with engine.begin() as conn:
        conn.execute(text("""Update employees set salary=:salary where name=:name"""),
                     {"salary":emp.salary,"name":name})
    return{"message":f"{name}'s salary updated to {emp.salary}"}

#Delete employee
@router.delete("/employees/{name}")
def delete_emp(name:str):
    with engine.begin() as conn:
        conn.execute(text("Delete from employees where name=:name"),{"name":name})
    return{"message":f"{name} deleted successfully!"}
        
    