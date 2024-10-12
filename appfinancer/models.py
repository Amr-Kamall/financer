from datetime import datetime
from appfinancer import db , login_mananger
from flask_login import UserMixin




@login_mananger.user_loader
def loa_user(user_id):
    return User.query.get(int(user_id)) 

class User(db.Model , UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    locationwork = db.Column(db.String(100), nullable=False)
     # علاقة الصادرات (One-to-Many)
    export_records = db.relationship('Exporttable', back_populates='user')
    
    # علاقة الواردات (One-to-Many)
    import_records = db.relationship('Importtable', back_populates='user')
    
    def __repr__(self):
        return f"User('{self.name}', '{self.username}', '{self.password}', '{self.locationwork}')"

class Exporttable(db.Model):
    __tablename__ = "exporttable"
    id = db.Column(db.Integer, primary_key=True)
    band = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.String(100), nullable=False)
    note = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(100), nullable=False , default = 'static/default.png')
    dates = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    times = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # حقل التعيين للمستخدم
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # علاقة المستخدم (Many-to-One)
    user = db.relationship('User', back_populates='export_records')
    
    def __repr__(self):
        return f"Exporttable('{self.band}', '{self.price}', '{self.amount}', '{self.note}', '{self.dates}', '{self.times}' , '{self.image_file}')"
    




class Importtable(db.Model):
    __tablename__ = "importtable"
    id = db.Column(db.Integer, primary_key=True)
    band = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.String(100), nullable=False)
    note = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(100), nullable=False , default = 'default.png')
    dates = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    times = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # حقل التعيين للمستخدم
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # علاقة المستخدم (Many-to-One)
    user = db.relationship('User', back_populates='import_records')
    
    def __repr__(self):
        return f"Importtable('{self.band}' , '{self.price}' ,'{self.amount}' ,'{self.note}' ,'{self.dates}' ,'{self.times}' , '{self.image_file}')"
