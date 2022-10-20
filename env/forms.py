from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class AddUserForm(FlaskForm):
    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired()])
    phone_number = StringField('Phone Number',
                                     validators=[DataRequired()])
    submit = SubmitField('Submit user')

class RemoveUserForm(FlaskForm):
    first_name = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Remove user')