from app import app
from db import debug

db.init_(app)

@app.before_first_request
def create_tables():
    db.create_all()
