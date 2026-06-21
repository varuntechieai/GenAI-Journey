employees=[
    {"name":"Ryan","salary":45000,"department":"HR"},
    {"name":"Alicia","salary":85000,"department":"Tech"},
    {"name":"Sara","salary":24000,"department":"HR"},
    {"name":"Conor","salary":54000,"department":"Finance"},
    {"name":"Mike","salary":22000,"department":"Tech"},
    {"name":"John","salary":64000,"department":"Tech"}
]

#Group by dept and count(*)
groups={}
for emp in employees:
    dept=emp["department"]
    if dept not in groups:
        groups[dept]=0
    groups[dept]+=1
print("Department | Count")
print("-"*20)
for dept,count in groups.items():
    print(f"{dept} | {count}")

#Second Table - Departments 
departments=[
    {"name":"HR","location":"New York"},
    {"name":"Tech","location":"Florida"},
    {"name":"Finance","location":"Miami"}
]

#Join employees-department on departments-name
print("\nDepartment | Name")
print("-"*25)
for emp in employees:
    for dept in departments:
        if emp["department"]==dept["name"]:
            print(f"{emp['name']} | {emp['department']} | {dept['location']}")

#Limit 3 - top 3 highest paid employees
print("\nTop 3 highest paid employee")
print("-"*35)
sort_emp=sorted(employees,key= lambda emp:emp["salary"],reverse=True)
top3=sort_emp[:3]
for emp in top3:
    print(f"{emp['name']} - {emp['salary']}")
