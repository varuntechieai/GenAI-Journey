import pandas as pd
#Creating a dataframe like SQL table
data={
    "name":["Ricky","Jennifer","Simon","Kathy","Donald"],
    "salary":[78000,42000,96500,35000,54000],
    "department":["Tech","HR","Tech","Finance","HR"]
}
df=pd.DataFrame(data)
print(df)

#Where salary>5000
print("\n---Where Salary>50000---")
print(df[df['salary']>50000])

#Order by salary desc
print("\n---Order by salary desc---")
print(df.sort_values("salary",ascending=False))

#Select count(*)
print("\n---Select Count(*)---")
print(f"Total Employees: {len(df)}")

#Avg salary
print("\n---Average Salary")
print(f"The average salary of employees is {df['salary'].mean(): .0f}")

#Group by department and count(*)
print("\n---Group by department---")
result=df.groupby("department")["name"].count().reset_index()
result.columns=["Department","Count"]
print(result)

#Limit 3
print("\n---Limit 3---")
print(df.head(3))

#Second table department
dept={
    "department":["HR","Tech","Finance"],
    "location":["New York","Florida","Miami"]
}
dept_df=pd.DataFrame(dept)
print("\n----Join----")
joined_df=df.merge(dept_df,on="department")
print(joined_df)

