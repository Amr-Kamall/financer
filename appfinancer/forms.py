from flask_wtf import FlaskForm
from wtforms import BooleanField, FileField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length , ValidationError
from appfinancer.models import User


class LoginFormadmin(FlaskForm):
    usernameadmin = StringField("Username", validators=[DataRequired(), Length(min=3, max=25)])
    passwordadmin = PasswordField(
        "Password", validators= [DataRequired() , Length( min = 8 , max = 16)]
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("دخول")



class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField(
        "Password", validators= [DataRequired() , Length( min = 8 , max = 16)]
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("دخول")

class AddForm(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(min=3, max=100)])
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField(
        "Password", validators= [DataRequired() , Length( min = 8 , max = 16)]
    )
    locationwork = StringField("Locationwork" , validators=[DataRequired()])
    submit = SubmitField("إضافة مستخدم جديد")
    
    def validate_username(self , username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('اسم المستخدم هذا موجود بالفعل  استخدم اسم اخر')


class ExportForm(FlaskForm):
    band = StringField("band", validators=[DataRequired()])
    price = IntegerField("price", validators=[DataRequired()])
    amount = IntegerField("amount", validators= [DataRequired()])
    note = TextAreaField("note" , default='الملاحظات')
    image_file = FileField("صورة")
    submit = SubmitField("أضافة")





class ImportForm(FlaskForm):
    band = StringField("band", validators=[DataRequired()])
    price = IntegerField("price", validators=[DataRequired()])
    amount = IntegerField("amount", validators= [DataRequired()])
    note = TextAreaField("note" , default='الملاحظات')
    image_file = FileField("صورة")
    submit = SubmitField("أضافة")




class Dropdown(FlaskForm):
    location = SelectField("location" , choices=[('option1', 'cairo'), ('option2', 'alex'), ('option3', 'abukabir')])
