from fastapi import FastAPI
from app.database import create_table
from app.routes import router

app=FastAPI(
    title="Employee Management API",
    description="A Rest API Built Using FastAPI + SqlAlchemy",
    version="1.0.0"
)

#Create table on startup
create_table()
#Include all routers
app.include_router(router)

@app.get("/")
def home():
    return{"message":"Welcome to Employee Management API! Go To /docs to explore."}