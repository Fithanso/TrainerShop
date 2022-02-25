from application import *
from flask import Blueprint, render_template, request, redirect, url_for

from global_settings.forms import CreateGlobalSettingForm, EditGlobalSettingForm
from global_settings.models.GlobalSetting import GlobalSettingModel, GlobalSettingModelRepository

from decorators import admin_only

global_settings = Blueprint('global_settings', __name__, template_folder='templates')


@global_settings.route('/create/', methods=['GET', 'POST'])
@admin_only
def create():
    form = CreateGlobalSettingForm()

    if form.validate_on_submit():
        form_data = request.form

        global_setting_id = GlobalSettingModelRepository.create_id()
        new_global_setting = GlobalSettingModel(id=global_setting_id, name=form_data['name'],
                                                value=form_data['value'])
        db.session.add(new_global_setting)
        db.session.commit()

        flash('Global setting created successfully', category='success')

        return redirect(url_for('admin_panel.display_all_global_settings'))

    return render_template('global_settings/create_global_setting.html', form=form)


@global_settings.route('/edit/<int:global_setting_id>', methods=['GET'])
@admin_only
def edit(global_setting_id):
    form = EditGlobalSettingForm()

    global_setting_entity = GlobalSettingModel.query.get(global_setting_id)

    form.name.data = global_setting_entity.name
    form.value.data = global_setting_entity.value
    form.global_setting_id.data = global_setting_id

    return render_template('global_settings/edit_global_setting.html', form=form, global_setting_id=global_setting_id)


@global_settings.route('/edit/', methods=['POST'])
@admin_only
def validate_edit():

    form = EditGlobalSettingForm()

    form_data = request.values

    if form.validate_on_submit():

        global_setting_entity = GlobalSettingModel.query.get(form_data['global_setting_id'])
        global_setting_entity.name = form_data['name']
        global_setting_entity.value = form_data['value']

        db.session.commit()

        flash('Global setting edited successfully', category='success')

    return redirect(url_for('admin_panel.display_all_global_settings'))


@global_settings.route('/delete/<int:global_setting_id>/', methods=['GET'])
@admin_only
def delete(global_setting_id):
    global_setting_entity = GlobalSettingModel.query.get(global_setting_id)

    db.session.delete(global_setting_entity)
    db.session.commit()

    flash('Global setting deleted successfully', category='success')

    return redirect(url_for('admin_panel.display_all_global_settings'))
