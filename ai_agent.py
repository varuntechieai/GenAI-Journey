from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ==================
# Tools
# ==================
def calculate(expression):
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def search_employee(name):
    employees = {
        "Varun": {"salary": 80000, "department": "Tech"},
        "Kenny": {"salary": 85000, "department": "Tech"},
        "Priya": {"salary": 24000, "department": "HR"},
        "Rahul": {"salary": 45000, "department": "HR"},
    }
    if name in employees:
        emp = employees[name]
        return f"{name} - Department: {emp['department']}, Salary: {emp['salary']}"
    return f"{name} not found"

def get_department_info(department):
    departments = {
        "Tech": "4 employees, average salary 77500",
        "HR": "3 employees, average salary 36000",
        "Finance": "1 employee, average salary 22000"
    }
    return departments.get(department, "Department not found")

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
run_agent("What is Varun's salary and which department does he work in?")
run_agent("What is 20% bonus on Kenny's salary?")
run_agent("Tell me about the Tech department")