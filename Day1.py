#Day 1 of my GenAI journey
employees=[
    {"name":"Rahul","salary":45000},
    {"name":"Kenny","salary":85000},
    {"name":"Priya","salary":24000},
    {"name":"Karan","salary":54000},
    {"name":"Ashu","salary":22000}
]
#where salary>30000
filtered=[emp for emp in employees if emp["salary"]>30000]
print("Name | Salary")
print("-" * 20)
for emp in filtered:
    print(f"{emp['name']} | {emp['salary']}")


#SQL select * from employees order by salary desc
sort_emp=sorted(employees,key=lambda emp:emp["salary"],reverse=True)
print("Name | Salary")
print("-"*20)
for emp in sort_emp:
    print(f"{emp['name']} | {emp['salary']}")

#Count(*) from employees
total=len(employees)
print(f"Total Employees: {total}")

#Avg of salary
avg_sal=sum(emp["salary"] for emp in employees) / len(employees)
print(f"Average salary of employees: {avg_sal: .0f}")