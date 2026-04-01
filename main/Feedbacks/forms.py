from flask_wtf import FlaskForm
from wtforms import RadioField,TextAreaField
from wtforms.validators import DataRequired,Length

class FeedbackForm(FlaskForm):
    rating = RadioField('Rating', coerce=int, choices=[
        (5, '★ ★ ★ ★ ★'), (4, '★ ★ ★ ★'), (3, '★ ★ ★'), (2, '★ ★'), (1, '★')
    ], validators=[DataRequired()])
    message = TextAreaField('Feedback', validators=[DataRequired(), Length(max=1000)])