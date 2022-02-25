from application import *
from flask import Blueprint, render_template, request, redirect, url_for

from shipment.forms import CreateShipmentMethodForm, EditShipmentMethodForm
from shipment.models.ShipmentMethod import ShipmentMethodModel, ShipmentMethodModelRepository

from decorators import admin_only

shipment = Blueprint('shipment', __name__, template_folder='templates')


@shipment.route('/create/', methods=['GET', 'POST'])
@admin_only
def create():
    form = CreateShipmentMethodForm()

    if form.validate_on_submit():
        form_data = request.form

        try:
            shipment_method_id = ShipmentMethodModelRepository.create_id()
            new_shipment_method = ShipmentMethodModel(id=shipment_method_id, cost=form_data['cost'], name=form_data['name'],
                                                      estimated_time=form_data['estimated_time'])
            db.session.add(new_shipment_method)
            db.session.commit()
            flash('Shipment method created successfully', category='success')
        except Exception as e:
            flash('Error occurred while creating a shipment method', category='error')
            return {"message": str(e)}

        return redirect(url_for('admin_panel.display_all_shipment_methods'))

    return render_template('shipment/create_shipment_method.html', form=form)


@shipment.route('/edit/<int:shipment_method_id>', methods=['GET'])
@admin_only
def edit(shipment_method_id):
    form = EditShipmentMethodForm()

    shipment_method_entity = ShipmentMethodModel.query.get(shipment_method_id)

    form.cost.data = shipment_method_entity.cost
    form.estimated_time.data = shipment_method_entity.estimated_time
    form.name.data = shipment_method_entity.name
    form.shipment_method_id.data = shipment_method_id

    return render_template('shipment/edit_shipment_method.html', form=form, shipment_method_id=shipment_method_id)


@shipment.route('/edit/', methods=['POST'])
@admin_only
def validate_edit():

    form = EditShipmentMethodForm()

    form_data = request.values

    if form.validate_on_submit():

        try:
            shipment_method_entity = ShipmentMethodModel.query.get(form_data['shipment_method_id'])
            shipment_method_entity.cost = form_data['cost']
            shipment_method_entity.estimated_time = form_data['estimated_time']
            shipment_method_entity.name = form_data['name']

            db.session.commit()

            flash('Shipment method edited successfully', category='success')

        except Exception as e:
            flash('Error occurred while editing a shipment method', category='error')
            return {"message": str(e)}
    return redirect(url_for('admin_panel.display_all_shipment_methods'))


@shipment.route('/delete/<int:shipment_method_id>/', methods=['GET'])
@admin_only
def delete(shipment_method_id):
    shipment_method_entity = ShipmentMethodModel.query.get(shipment_method_id)

    db.session.delete(shipment_method_entity)
    db.session.commit()

    flash('Shipment method edited successfully', category='success')

    return redirect(url_for('admin_panel.display_all_shipment_methods'))
