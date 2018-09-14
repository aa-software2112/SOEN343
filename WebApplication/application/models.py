from application import db

#Creating a basic User table with id and first name attributes
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(64), index=True, unique=True)


    def __repr__(self):
        return '<User: {}>'.format(self.fname)