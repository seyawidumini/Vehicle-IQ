from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,FileField
from wtforms.validators import DataRequired,Length
from flask_wtf.file import FileField, FileAllowed

class AddvehicleForm(FlaskForm):
    photo=FileField('Photo',validators=[DataRequired(),
            FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPG and PNG images allowed!')])
    brand=StringField('Brand',validators=[DataRequired(),Length(max=20)])
    model=StringField('Model',validators=[DataRequired(),Length(max=20)])
    vehicle_category=StringField('Cateogry',validators=[DataRequired(),Length(max=20)])
    fuel_type=StringField('Fule Type',validators=[DataRequired(),Length(max=20)])
    submit = SubmitField('Submit')
