import json

class Drink:
    def __init__(self, id, name, instructions=None):
        self._id = id
        self._name = name
        self._instructions = instructions

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_instructions(self):
        return self._instructions

    def set_instructions(self, instructions):
        self._instructions = instructions        

    id = property(get_id)
    name = property(get_name, set_name)
    instructions = property(get_instructions, set_instructions)

class Person:
    def __init__(self, id, first_name, last_name, fav_drink: Drink=None):
        self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._fav_drink = fav_drink


    def get_id(self):
        return self._id

    def get_first_name(self):
        return self._first_name

    def set_first_name(self, name):
        self._first_name = name

    def get_last_name(self):
        return self._last_name

    def set_last_name(self, name):
        self._last_name = name
   
    def get_fav_drink(self):
        return self._fav_drink

    def set_fav_drink(self, drink: Drink):
        self._fav_drink = drink
    
    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

     
    id = property(get_id)
    first_name = property(get_first_name, set_first_name)
    last_name = property(get_last_name, set_last_name)
    full_name = property(get_fullname)
    fav_drink = property(get_fav_drink, set_fav_drink)


class Round:
    def __init__(self, id, active, start_time_UTC, initiator):
        self.id = id
        self._orders = {}
        self._active = active
        self._start_time_UTC = start_time_UTC
        self.initiator = initiator

    def start(self):
        self._active = True
        #self._start_time_UTC = NOW
        self.save_round_state_on_start_and_return_id()

    def end(self):
        #ends round early
        self._active = False
 
    def update_order(self, person, drink):
        self._orders[person] = drink

    def isActive(self):
        return self._active

    def get_orders(self):
        return self._orders

    def set_orders(self, orders):
        self._orders = orders

    def get_start_time_UTC(self):
        return self._start_time_UTC          

    orders = property(get_orders, set_orders)
    start_time_UTC = property(get_start_time_UTC)
