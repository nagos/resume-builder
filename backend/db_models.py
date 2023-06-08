from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text())
    user = db.relationship("User")
