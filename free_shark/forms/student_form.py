from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired

class StudentForm(FlaskForm):
    user_id=StringField('user_id')
    school_number=StringField('school_number')
    real_name=StringField('real_name',validators=[DataRequired()])
    college=StringField('college',validators=[DataRequired()])
    banji=StringField('banji')
    contact=PasswordField('contact')