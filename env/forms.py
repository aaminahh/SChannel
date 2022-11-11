from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length

class AddNewUserForm(FlaskForm):
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

class CreateNewGroup(FlaskForm):
    group_name = StringField('Group Name',
                            validators=[DataRequired(), Length(min=2, max=30)])
    group_desc = TextAreaField('Group Description',
                            validators=[DataRequired(), Length(min=2, max=250)])
    group_add_existing = SelectField('Add existing user', 
                            choices = [])
    submit = SubmitField('Create group')
