from app import *
from flask import Blueprint, render_template, request, redirect, url_for
from decorators import admin_only
from global_settings.forms import CreateGlobalSettingForm, EditGlobalSettingForm
from global_settings.models.GlobalSetting import GlobalSettingModel, GlobalSettingModelRepository

global_settings = Blueprint('global_settings', __name__, template_folder='templates')


@global_settings.route('/create/', methods=['GET', 'POST'])
@admin_only
def create():
    form = CreateGlobalSettingForm()

    if form.validate_on_submit():
        data = request.form

        try:
            global_setting_id = GlobalSettingModelRepository.create_id()
            new_global_setting = GlobalSettingModel(id=global_setting_id, name=data['name'],
                                                    value=data['value'])
            db.session.add(new_global_setting)
            db.session.commit()
        except Exception as e:
            return {"message": str(e)}

        return redirect(url_for('admin_panel.list_global_settings'))

    return render_template('global_settings/create_global_setting.html', form=form)


@global_settings.route('/edit/<global_setting_id>', methods=['GET'])
@admin_only
def edit(global_setting_id):
    form = EditGlobalSettingForm()

    existing_global_setting = GlobalSettingModel.query.get(global_setting_id)

    form.name.data = existing_global_setting.name
    form.value.data = existing_global_setting.value
    form.global_setting_id.data = global_setting_id

    return render_template('global_settings/edit_global_setting.html', form=form, global_setting_id=global_setting_id)


@global_settings.route('/edit/', methods=['POST'])
@admin_only
def validate_edit():

    form = EditGlobalSettingForm()

    data = request.values

    if form.validate_on_submit():

        try:
            existing_global_setting = GlobalSettingModel.query.get(data['global_setting_id'])
            existing_global_setting.name = data['name']
            existing_global_setting.value = data['value']

            db.session.commit()

        except Exception as e:
            return {"message": str(e)}
    return redirect(url_for('admin_panel.list_global_settings'))


@global_settings.route('/delete/<global_setting_id>/', methods=['GET'])
@admin_only
def delete(global_setting_id):
    entity = GlobalSettingModel.query.get(global_setting_id)

    db.session.delete(entity)
    db.session.commit()

    return redirect(url_for('admin_panel.list_global_settings'))
