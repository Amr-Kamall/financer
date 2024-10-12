from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
from flask_migrate  import Migrate




app = Flask(__name__)
app.config['SECRET_KEY'] = '8c9dc66f5354bf342e89f2006db11663374f20cb5d61aefbb294c4f7794ffc5f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = 'appfinancer\static\images'  # المجلد الذي سيتم تخزين الصور فيه
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app , db)
login_mananger = LoginManager(app)
login_mananger.login_view = "index"
login_mananger.login_message_category = "info"
app.app_context().push()


from appfinancer import routes