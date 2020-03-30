from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired

class OrderForm(FlaskForm):
    user_id=StringField('id')
    commodity_id=StringField('commodity_id')
    commodity_name=StringField('commodity_name')
    buyer_id=StringField('buyer_id')
    school_number=StringField('school_number')
    #real_name=StringField('real_name',validators=[DataRequired()])
    status=StringField('status')
    create_time=PasswordField('create_time')