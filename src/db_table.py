from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    rating = db.Column(db.Integer)
