from order.models.Courier import CourierModel


import random


class TempCourier:
    def __init__(self):
        self.id = 0
        self.name = "Undefined courier"
        self.surname = "Undefined courier"
        self.patronymic = "Undefined courier"


class CourierAssigner:
    def get_available_courier(self):

        courier_entities = CourierModel.query.all()

        if not courier_entities:
            return TempCourier()

        return random.choice(courier_entities)



