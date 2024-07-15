from flask import Flask, render_template, request, redirect, url_for, session, flash
import importlib
import os
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired
import logging
from flask_wtf.csrf import CSRFProtect
# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'
csrf = CSRFProtect(app)
# Setup logging
logging.basicConfig(level=logging.DEBUG)

def load_filter_library():
    df = pd.read_excel('library/depth_filter_library.xlsx')
    filter_library = {}
    for _, row in df.iterrows():
        filter_library[row['type']] = {'area': row['area'], 'discard_volume': row['discard_volume']}
    return filter_library

@app.before_request
def load_libraries():
    if 'filter_library' not in session:
        session['filter_library'] = load_filter_library()

def camel_case(input_str):
    components = input_str.split('_')
    return components[0].capitalize() + ''.join(x.capitalize() for x in components[1:])

@app.route('/')
def index():
    form = UpstreamForm()
    modules = [name for name in os.listdir('modules') if os.path.isdir(os.path.join('modules', name))]
    return render_template('index.html', modules=modules,  form=form)

@app.route('/select_steps', methods=['POST'])
def select_steps():
    steps = request.form.getlist('steps')
    session['steps'] = steps
    print(steps)
    return redirect(url_for('upstream_inputs'))

@app.route('/upstream_inputs')
def upstream_inputs():
    form = UpstreamForm()
    return render_template('upstream_inputs.html', form=form)

@app.route('/calculate_upstream', methods=['POST'])
def calculate_upstream():
    form = UpstreamForm()
    if form.validate_on_submit():
        session['volume_in'] = form.volume_in.data
        session['mass_in'] = form.mass_in.data
        return redirect(url_for('calculate_step', step=0))
    return render_template('upstream_inputs.html', form=form)

@app.route('/calculate_step/<int:step>', methods=['GET', 'POST'])
def calculate_step(step):
    steps = session.get('steps', [])
    if step >= len(steps):
        return redirect(url_for('results'))

    current_step = steps[step]
    logging.debug(f"Current step: {current_step}")
    module = importlib.import_module(f'modules.{current_step}.forms')
    FormClass = getattr(module, f'{camel_case(current_step)}Form')
    filter_library = session.get('filter_library', {})
    form = FormClass(filter_library)

    if form.validate_on_submit():
        # 动态加载模块计算函数
        module_calc = importlib.import_module(f'modules.{current_step}.calculations')
        calculate_func = getattr(module_calc, f'calculate_{current_step}')

        # 动态获取表单字段，排除提交按钮
        form_data = {field.name: field.data for field in form if field.name != 'submit'}
        volume_in = session.get('volume_in')
        mass_in = session.get('mass_in')

        # 调用计算函数
        results = calculate_func(volume_in, mass_in, filter_library, **form_data)
        logging.debug(f"Results: {results}")

        # 存储结果到 session 中
        session['volume_in'] = results['volume_out']
        session['mass_in'] = results['mass_out']
        session.update(results)

        return redirect(url_for('calculate_step', step=step + 1))
    else:
        logging.debug(f"Form errors: {form.errors}")

    return render_template('step.html', form=form, step=current_step)

@app.route('/results')
def results():
    return render_template('results.html', results=session)

class UpstreamForm(FlaskForm):
    volume_in = FloatField('Upstream Volume (L)', validators=[DataRequired()])
    mass_in = FloatField('Upstream Mass (g)', validators=[DataRequired()])
    submit = SubmitField('Next')

if __name__ == '__main__':
    app.run(debug=True)
