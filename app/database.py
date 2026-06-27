from sqlalchemy import create_engine,text
import os

Base_DIR=os.path.dirname(os.path.abspath(__file__))
DB_Path=os.path.join(Base_DIR,"..","employee_mgmt.db")

engine=create_engine(f"sqlite:///{DB_Path}",echo=False)

def create_table():
    with engine.begin() as conn:
        conn.execute(text("""Create table if not exists employees(
                          id Integer Primary Key AUTOINCREMENT,
                          name text not null,
                          salary real not null,
                          department text not null)"""))
    print("Database is ready !")
    