from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,RadioField,TextAreaField,IntegerField,SelectField,FloatField,BooleanField,FileField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError,NumberRange
from main.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username=StringField("Username",
                         validators=[DataRequired(),Length(min=2,max=20)])
    
    email=StringField("Email",
                      validators=[DataRequired(),Email()])
    
    password=PasswordField("Password",
                           validators=[DataRequired()])
    
    confirm_password=PasswordField("Confirm Password",
                           validators=[DataRequired(),EqualTo("password")])
    
    submit=SubmitField("Sign up")

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("username is taken")
        
    def validate_email(self,email):
        email=User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email is taken")


class LoginForm(FlaskForm):
    email=StringField("Email",
                      validators=[DataRequired(),Email()])
    
    password=PasswordField("Password",
                           validators=[DataRequired()])
    
    submit=SubmitField("Login")

class AdminLoginForm(FlaskForm):
    email=StringField("Email",
                      validators=[DataRequired(),Email()])
    
    password=PasswordField("Password",
                           validators=[DataRequired()])
    
    submit=SubmitField("Login")

class FeedbackForm(FlaskForm):
    rating = RadioField('Rating', coerce=int, choices=[
        (5, '★ ★ ★ ★ ★'), (4, '★ ★ ★ ★'), (3, '★ ★ ★'), (2, '★ ★'), (1, '★')
    ], validators=[DataRequired()])
    message = TextAreaField('Feedback', validators=[DataRequired(), Length(max=1000)])

class BudgetRequestForm(FlaskForm):
    budget=IntegerField("Budget",validators=[DataRequired()])


class VehiclePredictionForm(FlaskForm):
    model_year = IntegerField(
        "Model Year",
        validators=[DataRequired(), NumberRange(min=1980, max=2026)])
    
    milage = IntegerField(
        "Mileage (km)",
        validators=[DataRequired(), NumberRange(min=0)])

    transmission = SelectField(
    "Transmission",
    validators=[DataRequired()],  
    choices=[("1", "Manual"), ("0", "Auto")]
    )

    condition = SelectField(
    "Condition",
    validators=[DataRequired()],
    choices=[("1","Mint"), ("0","Medium")]
    )
    
    cc = IntegerField(
        "Engine CC",
        validators=[DataRequired(), NumberRange(min=600, max=5000)])

    age = IntegerField(
        "Vehicle Age",
        validators=[DataRequired(), NumberRange(min=0, max=50)])

    power_steering = BooleanField("Power Steering")
    push_start = BooleanField("Push Start")

    car_model = SelectField(
        "Car Model",
        validators=[DataRequired()],
        choices=[
            ("model_aqua", "Toyota Aqua"),
            ("model_aqua urban", "Toyota Aqua Urban"),
            ("model_corolla 121 g grade", "Corolla 121 G Grade"),
            ("model_corolla 121 lx grade", "Corolla 121 LX Grade"),
            ("model_corolla 121 x grade", "Corolla 121 X Grade"),
            ("model_toyota axio g grade", "Toyota Axio G Grade"),
            ("model_toyota axio wxb", "Toyota Axio WXB"),
            ("model_toyota premio", "Toyota Premio"),
            ("model_toyota premio g superior", "Premio G Superior"),
            ("model_vitz", "Toyota Vitz"),
            ("model_vitz safety", "Toyota Vitz Safety"),
            ("model_yaris", "Toyota Yaris"),
        ]
    )

    fuel_type = SelectField(
        "Fuel Type",
        validators=[DataRequired()],
        choices=[
            ("fuel_type_petrol", "Petrol"),
            ("fuel_type_diesel", "Diesel"),
            ("fuel_type_hybrid", "Hybrid"),
        ]
    )

    location = SelectField(
        "Location",
        validators=[DataRequired()],
        choices=[
            ("location_colombo", "Colombo"),
            ("location_galle", "Galle"),
            ("location_gampaha", "Gampaha"),
            ("location_homagama", "Homagama"),
            ("location_kadawatha", "Kadawatha"),
            ("location_kaluthara", "Kaluthara"),
            ("location_kandy", "Kandy"),
            ("location_kurunagala", "Kurunagala"),
            ("location_kurunegala", "Kurunegala"),
            ("location_maharagama", "Maharagama"),
            ("location_malabe", "Malabe"),
            ("location_matara", "Matara"),
            ("location_nugegoda", "Nugegoda"),
            ("location_others", "Others"),
            ("location_panadura", "Panadura"),
            ("location_piliyandala", "Piliyandala"),
            ("location_polonnaruwa", "Polonnaruwa"),
            ("location_rathnapura", "Rathnapura"),
        ]
    )

    vehicle_type = SelectField(
        "Vehicle Type",
        validators=[DataRequired()],
        choices=[
            ("car/sedan_car", "Car"),
            ("car/sedan_sedan", "Sedan"),
        ]
    )

    color = SelectField(
        "Exterior Color",
        validators=[DataRequired()],
        choices=[
            ("ext_col_ash", "Ash"),
            ("ext_col_black", "Black"),
            ("ext_col_dark blue", "Dark Blue"),
            ("ext_col_desert sand mica", "Desert Sand Mica"),
            ("ext_col_grey", "Grey"),
            ("ext_col_lunar mist", "Lunar Mist"),
            ("ext_col_others", "Others"),
            ("ext_col_pearl white", "Pearl White"),
            ("ext_col_red", "Red"),
            ("ext_col_super white", "Super White"),
            ("ext_col_white", "White"),
            ("ext_col_wine red", "Wine Red"),
        ]
    )
    submit = SubmitField("Predict Price")

class AddvehicleForm(FlaskForm):
    photo=FileField('Photo',validators=[DataRequired()])
    brand=StringField('Brand',validators=[DataRequired(),Length(max=20)])
    model=StringField('Model',validators=[DataRequired(),Length(max=20)])
    vehicle_category=StringField('Cateogry',validators=[DataRequired(),Length(max=20)])
    fuel_type=StringField('Fule Type',validators=[DataRequired(),Length(max=20)])
    submit = SubmitField('Submit')

class AddBudgetForm(FlaskForm):
    model=StringField('Model',validators=[DataRequired(),Length(max=20)])
    year=StringField('Year',validators=[DataRequired(),Length(max=20)])
    price=IntegerField('Price',validators=[DataRequired()])
    submit = SubmitField('Submit')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')