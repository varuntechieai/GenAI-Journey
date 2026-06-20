#Day 1 of my GenAI journey
employees=[
    {"name":"Rahul","salary":45000},
    {"name":"Varun","salary":8500000},
    {"name":"Priya","salary":24000},
    {"name":"Karan","salary":15000},
    {"name":"Ashu","salary":22000}
]
#where salary>30000
filtered=[emp for emp in employees if emp["salary"]>30000]
print("Name | Salary")
print("-" * 20)
for emp in filtered:
    print(f"{emp['name']} | {emp['salary']}")
