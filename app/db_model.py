from app import db


class TMQuery(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    year = db.Column(db.Integer(), nullable=True)
    odometer = db.Column(db.Integer(), nullable=True)
    price = db.Column(db.Integer(), nullable=True)

    def __repr__(self):
        return f"TMQuery('{self.year}', '{self.odometer}', '{self.price}')"