from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired

class DepthFiltrationForm(FlaskForm):
    def __init__(self, filter_library, *args, **kwargs):
        super(DepthFiltrationForm, self).__init__(*args, **kwargs)
        self.filter_type.choices = [(filter_type, filter_type) for filter_type in filter_library.keys()]
    
    filter_type = SelectField('Filter Type', validators=[DataRequired()])
    harvest_filter_loading_capacity = FloatField('Harvest Filter Loading Capacity (L/m²)', validators=[DataRequired()])
    harvest_depth_filtration_yield = FloatField('Harvest Depth Filtration Yield (%)', validators=[DataRequired()])
    harvest_filter_wfi_flux_requirement = FloatField('Harvest Filter WFI Flux Requirement (LMH)', validators=[DataRequired()])
    harvest_wfi_volume_per_filter_area = FloatField('Harvest WFI Volume Per Filter (L/m²)', validators=[DataRequired()])
    harvest_equilibration_volume_per_filter_area = FloatField('Harvest Equilibration Volume Per Filter (L/m²)', validators=[DataRequired()])
    harvest_chase_volume_per_filter_area = FloatField('Harvest Chase Volume Per Filter (L/m²)', validators=[DataRequired()])
    harvest_filter_process_flux_requirement = FloatField('Harvest Filter Process Flux Requirement (LMH)', validators=[DataRequired()])
    submit = SubmitField('Next')
