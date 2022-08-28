from pythonRest import db
import os
import uuid
from dotenv import load_dotenv

load_dotenv()
admin_pass = os.getenv('ADMIN_PASSWORD') 

basedir = os.path.abspath(os.path.dirname(__file__))

def create_db():
    from pythonRest import User, db
    db.create_all()
    id = uuid.uuid1()
    unique_hash = id.hex
    new_user = User("admin", admin_pass, unique_hash)
    db.session.add(new_user)
    db.session.commit()

if os.path.exists(os.path.join(basedir, 'database.sqlite')):
    if input("Database already exists, do you want to delete existing database and create new one? (y/n)").lower() == "y":
        os.remove(os.path.join(basedir, 'database.sqlite')) 
        create_db()
        print("Database created")
        
    else:
        print("Leaving existing database")
else:
        create_db()
        print("Database created")        
