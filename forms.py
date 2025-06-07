from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo, ValidationError
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class PredictionForm(FlaskForm):
    beam_type = SelectField('Beam Type', 
                           choices=[('MULI', 'MULI'), ('MESSY', 'MESSY'), ('MANGA', 'MANGA'), ('MESS', 'MESS')],
                           validators=[DataRequired()])
    
    length_mm = FloatField('Length (mm)', 
                          validators=[DataRequired(), NumberRange(min=100, max=10000, message="Length must be between 100-10000 mm")])
    
    width_mm = FloatField('Width (mm)', 
                         validators=[DataRequired(), NumberRange(min=50, max=1000, message="Width must be between 50-1000 mm")])
    
    depth_mm = FloatField('Depth (mm)', 
                         validators=[DataRequired(), NumberRange(min=50, max=1000, message="Depth must be between 50-1000 mm")])
    
    reinforcement_percent = FloatField('Reinforcement (%)', 
                                     validators=[DataRequired(), NumberRange(min=0.1, max=10, message="Reinforcement must be between 0.1-10%")])
    
    load_kn = FloatField('Load (kN)', 
                        validators=[DataRequired(), NumberRange(min=0, max=100, message="Load must be between 0-100 kN")])
    
    submit = SubmitField('Predict Deflection')
