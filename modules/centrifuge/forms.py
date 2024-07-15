from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired

class CentrifugeForm(FlaskForm):
    pcv = FloatField('PCV (%)', validators=[DataRequired()])
    centrifuge_flush_volume = FloatField('Centrifuge Flush Volume (L)', validators=[DataRequired()])
    centrifuge_yield = FloatField('Centrifuge Yield (%)', validators=[DataRequired()])
    submit = SubmitField('Next')
