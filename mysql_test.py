from app import create_app,db

app = create_app('testdb')
app_context = app.app_context()
app_context.push()

db.drop_all()
db.create_all()