from flask_wtf import FlaskForm
from h11 import Data
from wtforms import DateField, StringField, DateTimeField,PasswordField, SubmitField , FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message="Name is required"),
        Length(min=2, max=20, message="Name must be between 2 and 20 characters")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address")
    ])
    number = StringField('Phone Number', validators=[
        DataRequired(message="Phone number is required"),
        Length(min=10, max=15, message="Please enter a valid phone number")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('password', message="Passwords must match")
    ])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required")
    ])
    submit = SubmitField('Log In')

class ServiceBookingForm(FlaskForm):
    pass

class ServiceCreationForm(FlaskForm):
    name = StringField('Service Name', validators=[
        DataRequired(message="Service name is required"),
        Length(min=2, max=50, message="Service name must be between 2 and 50 characters")
    ])
    description = StringField('Service Description', validators=[
        DataRequired(message="Service description is required"),
        Length(min=10, max=500, message="Description must be between 10 and 500 characters")
    ])
    price = StringField('Service Price', validators=[
        DataRequired(message="Price is required")
    ])
    location = StringField('Location', validators=[
        DataRequired(message="Location is required"),
        Length(max=200, message="Location must not exceed 200 characters")])
    # You might want to add an image field for service icon/image
    submit = SubmitField('Create Service')

class UpdateProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Location', validators=[Length(max=100)])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    submit = SubmitField('Update Profile')

class ServiceEditForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired()])
    description = StringField('Service Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Update Service')

class ServiceBookingForm(FlaskForm):
    # These fields will be disabled/readonly in the form
    name = StringField('Service Name', render_kw={'readonly': True})
    description = StringField('Service Description', render_kw={'readonly': True})
    price = FloatField('Price', render_kw={'readonly': True})
    location = StringField('Location', render_kw={'readonly': True})
    
    # Only these fields will be editable
    booking_date = DateTimeField('Preferred Date and Time', 
                                format='%Y-%m-%dT%H:%M',
                                validators=[DataRequired(message="Please select a date and time")])
    
    submit = SubmitField('Confirm Booking')