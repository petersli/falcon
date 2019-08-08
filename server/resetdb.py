from server import app, db
import os

os.system("rm database.db")
db.create_all()