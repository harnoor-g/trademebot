from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import NumberRange, InputRequired


class TradeMeQuery(FlaskForm):
    year = IntegerField('Year', validators=[InputRequired(), NumberRange(min=1900, max=2021)])
    price = IntegerField('Price', validators=[InputRequired(), NumberRange(min=0, max=9_999_999)])
    odometer = IntegerField('Odometer', validators=[InputRequired(), NumberRange(min=0, max=9_999_999)])
    submit = SubmitField('Submit Query')