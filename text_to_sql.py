from groq import Groq
from sqlalchemy import create_engine,text
from dotenv import load_dotenv
import os
import pandas as pd

#load env variables
load_dotenv()

#Setup
client=Groq(api_key=os.getenv("GROQ_API_KEY"))
engine=create_engine(f"sqlite:///company.db",echo=False,connect_args={"detect_types": 1})

#Create and populate database
def setup_db():
    with engine.begin() as conn:
        conn.execute(text("""Create table if not exists employees(
                          ID integer primary key autoincrement,
                          Name text not null,
                          Salary real not null,
                          Department text not null)"""))
        conn.execute(text("Delete from employees"))
        employees_data=[
            {"name":"Frank","salary":45000,"department":"HR"},
            {"name":"Kenny","salary":85000,"department":"Tech"},
            {"name":"Alicia","salary":24000,"department":"HR"},
            {"name":"Sean","salary":54000,"department":"Tech"},
            {"name":"Johnny","salary":80000,"department":"Tech"},
            {"name":"Kane","salary":22000,"department":"Finance"},
            {"name":"Luke","salary":67000,"department":"Tech"},
            {"name":"Sonya","salary":39000,"department":"HR"},
        ]
        for emp in employees_data:
            conn.execute(text("""Insert into employees(name,salary,department)
                              values(:name,:salary,:department)"""),emp)
    print("Database is ready!")
setup_db()

#Step 1 - Convert natural language to sql using Llama 3
def natural_lang_sql(user_question):
    prompt= f"""
You are a SQLite expert. Given the table schema below, 
write a SQL query that answers the question.

Schema:
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    salary REAL,
    department TEXT
)

Sample data:
- departments are exactly: 'HR', 'Tech', 'Finance'
- salaries are numbers like 45000, 85000

Return ONLY the SQL query. No explanations. No markdown. No backticks.Also give the alias to result as columns like for count-Total count and likewise


    Question: {user_question}

    SQL:
    """
    response=client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        messages=[
            {"role":"system","content":"You are a SQL query generator. You only output raw SQL queries. Nothing else. No explanations. No markdown."},
            {"role":"user","content":prompt}
        ]
    )
    return response.choices[0].message.content.strip()

#Step 2-Execute the generated SQL to real DB
def execute_sql(sql_query):
    try:
        with engine.begin() as conn:
            result=conn.execute(text(sql_query))
            df=pd.DataFrame(result.fetchall(),columns=result.keys())
        return df
    except Exception as e:
        return f" Error executing sql: {str(e)}"

#Tep 3 - Combine both into one function
def ask_database(user_question):
    print(f"\n Question: {user_question}")

    #Convert into SQL
    sql=natural_lang_sql(user_question)
    print(f" Generated sql: {sql}")

    #Execute sql
    result=execute_sql(sql)
    print(f"Result:")
    print(result)
    return result

#Test with questions
# ask_database("Show me all employees in Tech department")
# ask_database("Who is the highest paid employee?")
# ask_database("Show me average salary by department")
# ask_database("How many employees are in each department?")
# ask_database("Show me employees earning more than 50000")
# ask_database("Who earns the least in HR department?")

# =====================
# Interactive Chat Loop
# =====================
def chat_loop():
    print("="*50)
    print("🤖 Text to SQL AI Assistant")
    print("Ask questions about your employee database")
    print("Type 'exit' to quit")
    print("="*50)

    while True:
        user_question=input("\n💬 You: ")
        if user_question.lower()=="exit":
            print("👋 Goodbye Varun")
            break
        ask_database(user_question)
#Run the chat
chat_loop()
