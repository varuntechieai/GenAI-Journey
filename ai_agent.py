from groq import Groq
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine,text
import pandas as pd

#Setup tool database
engine=create_engine("sqlite:///agent.db",echo=False)

def setup_database():
    with engine.begin() as conn:
        conn.execute(text("""
            Create table if not exists employees(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                salary REAL NOT NULL,
                department TEXT NOT NULL,
                experience INTEGER NOT NULL)"""))
        conn.execute(text("Delete from employees"))
        employees_data = [
            {"name": "Varun", "salary": 80000, "department": "Tech", "experience": 6},
            {"name": "Kenny", "salary": 85000, "department": "Tech", "experience": 8},
            {"name": "Priya", "salary": 24000, "department": "HR", "experience": 2},
            {"name": "Rahul", "salary": 45000, "department": "HR", "experience": 4},
            {"name": "Karan", "salary": 54000, "department": "Tech", "experience": 5},
            {"name": "Ashu", "salary": 22000, "department": "Finance", "experience": 1},
            {"name": "Rita", "salary": 67000, "department": "Tech", "experience": 7},
            {"name": "Sneha", "salary": 39000, "department": "HR", "experience": 3},
        ]

        for emp in employees_data:
            conn.execute(text("""
                INSERT INTO employees (name, salary, department, experience)
                VALUES (:name, :salary, :department, :experience)
            """), emp)

    print("✅ Database ready!")

setup_database()

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ==================
# Real Database Tools
# ==================
def search_employee(name):
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT name, salary, department, experience 
            FROM employees 
            WHERE name = :name
        """), {"name": name})
        row = result.fetchone()
    
    if row:
        return f"{row[0]} - Department: {row[2]}, Salary: {row[1]}, Experience: {row[3]} years"
    return f"{name} not found"

def get_department_info(department):
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT 
                COUNT(*) as total,
                AVG(salary) as avg_salary,
                MAX(salary) as max_salary,
                MIN(salary) as min_salary
            FROM employees
            WHERE department = :department
        """), {"department": department})
        row = result.fetchone()
    
    if row and row[0] > 0:
        return f"{department} - Total: {row[0]} employees, Avg Salary: {round(row[1])}, Max: {row[2]}, Min: {row[3]}"
    return f"Department {department} not found"

def get_all_employees():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT name, salary, department, experience FROM employees"))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df.to_string()

def calculate(expression):
    try:
        result = eval(expression)
        return str(round(float(result), 2))
    except Exception as e:
        return f"Error: {str(e)}"

# ==================
# Agent
# ==================
def run_agent(user_request):
    print(f"\n{'='*50}")
    print(f"🤔 Request: {user_request}")
    print(f"{'='*50}")

    system_prompt = """You are a helpful AI assistant with access to these tools:

TOOLS:
- search_employee("name") → returns employee salary and department
- get_department_info("department") → returns department statistics
- get_all_employees() → returns all employees list
- calculate("expression") → calculates math using numbers only

STRICT RULES:
- Call ONE tool at a time
- Use EXACT format: tool_name("input")
- Wait for ACTUAL tool result before continuing
- NEVER guess or assume tool results
- For bonus: FIRST call search_employee to get salary, THEN call calculate
- When you have all information, write: FINAL: your answer

Example:
User: What is Varun's salary?
Assistant: search_employee("Varun")
Tool Result: Varun - Department: Tech, Salary: 80000
FINAL: Varun's salary is 80000 and he works in Tech department."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_request}
    ]

    for step in range(5):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            temperature=0,
            messages=messages
        )

        reply = response.choices[0].message.content.strip()
        print(f"\n⚙️ Step {step+1}: {reply}")

        # Check for final answer first
        if "FINAL:" in reply:
            final_answer = reply.split("FINAL:")[-1].strip()
            print(f"\n✅ Final Answer: {final_answer}")
            return final_answer

        # Detect and execute tool calls
        tool_result = None

        if 'search_employee("' in reply:
            name = reply.split('search_employee("')[1].split('"')[0]
            tool_result = search_employee(name)

        elif 'get_department_info("' in reply:
            dept = reply.split('get_department_info("')[1].split('"')[0]
            tool_result = get_department_info(dept)
        
        elif 'get_all_employees()' in reply:
            tool_result = get_all_employees()

        elif 'calculate("' in reply:
            expr = reply.split('calculate("')[1].split('"')[0]
            tool_result = calculate(expr)

        if tool_result:
            print(f"🔧 Tool Result: {tool_result}")
            messages.append({"role": "assistant", "content": reply})
            messages.append({
                "role": "user",
                "content": f"Tool Result: {tool_result}\nNow continue. Use this EXACT result, never guess."
            })
        else:
            # No tool called and no FINAL — add response and continue
            messages.append({"role": "assistant", "content": reply})
            messages.append({
                "role": "user",
                "content": "Please call a tool or provide FINAL answer."
            })

    return "Could not complete task"

# ==================
# Test
# ==================
run_agent("What is Varun's salary and experience?")
run_agent("Compare HR and Tech departments")
run_agent("Who has the most experience in Tech?")
run_agent("What is 30% bonus on Rita's salary?")