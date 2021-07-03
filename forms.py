from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from wtforms.widgets import TextArea

class AddPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    picture = FileField('Add a picture', validators=[ FileAllowed(['jpg', 'png','jpeg'])])
    content = StringField('Description', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField()


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15, message="Your phone number should be more than 10 digits and less than 15")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Your passwords dont match, please try again')])
    submit = SubmitField('Sign Up')

    # def validate_phone(self, phone):
    #     user = User.query.filter_by(phone=phone.data).first()
    #     if user:
    #         raise ValidationError('That phone number is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class FeedbackForm(FlaskForm):
    phone = StringField('Phone')
    feedback = StringField('Feedback', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
