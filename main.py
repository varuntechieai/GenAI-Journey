from fastapi import FastAPI
app=FastAPI()
# @app.get("/")
# def home():
#     return{"message":"Welcome to employee api!"}

from sqlalchemy import create_engine, text
import pandas as pd

engine=create_engine("sqlite:///employee_mgmt.db",echo=False)

@app.get("/employees")
def get_emp():
    with engine.begin() as conn:
        result=conn.execute(text("Select * from employees"))
        df=pd.DataFrame(result.fetchall(),columns=result.keys())
    return df.to_dict(orient="records")

from pydantic import BaseModel

#This defines what data my API expects
class Employee(BaseModel):
    name: str
    salary: float
    department: str

#Post-add employee
@app.post("/employees")
def add_emp(emp: Employee):
    with engine.begin() as conn:
        conn.execute(text("""Insert into employees(name,salary,department) 
                          values(:name,:salary,:department)"""),{"name":emp.name,"salary":emp.salary,"depatment":emp.department})
    return {"message": f"{emp.name} added successfully!"}

#Put-update salary
@app.put("/employees/{name}")
def update_sal(name: str,salary: float):
    with engine.begin() as conn:
        conn.execute(text("""Update employees set salary=:salary where name=:name"""),
                     {"salary":salary,"name":name})
    return{"message":f"{name} updated salary is {salary}"}

#Delete- remove employee
@app.delete("/employees/{name}")
def del_emp(name: str):
    with engine.begin() as conn:
        conn.execute(text("Delete from employees where name=:name"),{"name":name})
    return{"message":f"Record for {name} has been deleted!"}



