from pydantic import BaseModel

class Employee(BaseModel):
    name: str
    salary: float
    department: str

class EmployeeUpdate(BaseModel):
    salary: float
    
