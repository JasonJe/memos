from app import db

class DataTable(db.Model):
    __tablename__ = 'data_table'
    test_id = db.Column('test_id', db.Integer, autoincrement = True, primary_key=True)
    test = db.Column('test', db.String)