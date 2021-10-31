import json
from flask import render_template, url_for, flash, redirect
from app import app, db
from app.form import TradeMeQuery
from app.db_model import TMQuery
from app.tmbot import run_bot


@app.route('/')
@app.route('/vehicles')
def vehicles():
    with open('./data/vehicle-data.json') as data:
        vehicles = json.load(data)
    return render_template('vehicles.html', title='Vehicles', vehicles=vehicles)

@app.route('/query', methods=['GET', 'POST'])
def vehicle_query():
    form = TradeMeQuery()
    if form.validate_on_submit(): 
        tm_query = TMQuery(year=form.year.data, odometer=form.odometer.data, price=form.price.data)
        db.session.add(tm_query)
        db.session.commit()
        run_bot(year_wanted=form.year.data, kms_wanted=form.odometer.data, price_wanted=form.price.data)
        flash('Query Submitted!', 'success')
        return redirect(url_for('vehicles'))
    return render_template('query.html', title='Vehicle Query', form=form)