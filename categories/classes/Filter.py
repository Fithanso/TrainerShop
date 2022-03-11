from application import db

from categories.models.Category import CategoryModel
from categories import funcs

from models import Characteristic

from abc import ABC, abstractmethod
import json


class FilterCreator:

    def __init__(self, category_entity, previous_filters):
        self.category_entity = category_entity
        self.raw_previous_filters = previous_filters

    def get_filters(self):
        charc_entities = self.category_entity.characteristics

        filters = []
        for charc in charc_entities:
            filter_unit = FilterForDisplay(charc.id, charc.name, charc.type)
            filter_unit.options = self.get_filter_options(charc)
            filters.append(filter_unit)

        return filters

    def get_filter_options(self, characteristic_entity):
        counter = 0
        result_list = []
        value_options_list = self.get_all_possible_values_from_products(characteristic_entity)

        for filter_option in value_options_list:
            option_name = self.make_input_name_from_id(characteristic_entity.id, counter)
            option_active = "checked" if option_name in self.raw_previous_filters else ""
            result_list.append(FilterOption(option_name, filter_option, option_active))

            counter += 1

        return result_list

    def get_all_possible_values_from_products(self, characteristic_entity):
        product_entities = self.category_entity.products

        filter_options = []
        for entity in product_entities:
            c_dict = json.loads(entity.characteristics)

            if funcs.characteristic_exists_in_product(characteristic_entity.id, c_dict):
                value = c_dict[str(characteristic_entity.id)]
                if value.strip() != '':
                    filter_options.append(value)

        return set(filter_options)

    def make_input_name_from_id(self, c_id, counter):
        return 'filter_' + str(c_id) + "_" + str(counter)


class FilterForDisplay:
    def __init__(self, c_id, c_name, c_type):
        self.characteristic_id = c_id
        self.name = c_name
        self.type = c_type
        self.options = []

    def __repr__(self):
        return f"<FilterForDisplay {self.__dict__}>"


class FilterOption:
    def __init__(self, name, value, active):
        self.name = name
        self.value = value
        self.active = active

    def __repr__(self):
        return f"<FilterOption {self.__dict__}>"


class FilterApplier:
    def __init__(self, product_entities, filters_dict):
        self.products = product_entities
        self.raw_filters = filters_dict
        self.filtering_units = self.create_filtering_units()

    def create_filtering_units(self):

        filtering_units = []
        grouped_values = self.group_filter_values_by_ids()

        for filter_id, values in grouped_values.items():
            if len(values) == 1:
                filtering_unit = OneValueFilter(filter_id, values[0])
            else:
                filtering_unit = MultipleValueFilter(filter_id, values)

            filtering_units.append(filtering_unit)

        return filtering_units

    def group_filter_values_by_ids(self):

        grouped_values = {}

        for key, value in self.raw_filters.items():
            filter_id = key.split("_")[0]
            if filter_id in grouped_values:
                grouped_values[filter_id].append(value)
            else:
                grouped_values[filter_id] = [value]

        return grouped_values

    def apply_filters(self):

        suitable_products = []

        for product in self.products:
            boolean_filtering_results = []

            for filtering_unit in self.filtering_units:
                boolean_filtering_results.append(filtering_unit.entity_suitable(product))

            all_filters_passed = all(boolean_filtering_results)

            if all_filters_passed:
                suitable_products.append(product)

        return suitable_products


class Filter(ABC):

    @abstractmethod
    def entity_suitable(self, entity):
        pass


class OneValueFilter(Filter):

    def __init__(self, filter_id, value):
        self.filter_id = filter_id
        self.value = value

    def entity_suitable(self, entity):
        c_dict = json.loads(entity.characteristics)

        if funcs.characteristic_exists_in_product(self.filter_id, c_dict):
            if c_dict[self.filter_id] == self.value:
                return True

        return False


class MultipleValueFilter(Filter):

    def __init__(self, filter_id, values):
        self.filter_id = filter_id
        self.values = values

    def entity_suitable(self, entity):
        c_dict = json.loads(entity.characteristics)

        if funcs.characteristic_exists_in_product(self.filter_id, c_dict):
            if c_dict[self.filter_id] in self.values:
                return True

        return False








