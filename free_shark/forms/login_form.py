from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField,PasswordField, SubmitField,BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username=StringField(label='用户名',validators=[DataRequired()])
    password=PasswordField(label='密码',validators=[DataRequired()])
    remember=BooleanField(label='记住我')
    submit=SubmitField(label="登录")