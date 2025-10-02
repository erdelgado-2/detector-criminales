from abc import ABC, abstractmethod


class State(ABC):

    @abstractmethod
    def transition(self, distance):
        pass

    def __eq__(self, object):
        if type(self) is type(object):
            return True
        else:
            return False


class Adentro(State):
    @staticmethod
    def adentro_a_calle():
        return "La criatura ha pasado de adentro a la calle"

    def transition(self, distance):
        if distance >= -150:
            self.transition_function = self.adentro_a_calle
            return Calle()
        else:
            return self

    def __str__(self):
        return "Adentro"


class Calle(State):
    @staticmethod
    def calle_a_afuera():
        return "La criatura ha pasado de la calle a afuera"

    @staticmethod
    def calle_a_adentro():
        return "La criatura ha pasado de la calle a adentro"

    def transition(self, distance):
        if distance > 150:
            self.transition_function = self.calle_a_afuera
            return Afuera()
        elif distance < -150:
            self.transition_function = self.calle_a_adentro
            return Adentro()
        else:
            return self

    def __str__(self):
        return "Calle"


class Afuera(State):
    @staticmethod
    def afuera_a_calle():
        return "La criatura ha pasado de afuera a la calle"

    def transition(self, distance):
        if distance <= 150:
            self.transition_function = self.afuera_a_calle
            return Calle()
        else:
            return self

    def __str__(self):
        return "Afuera"


class StateKeeper:
    @staticmethod
    def empty_event_function():
        return "No hay eventos que reportar"

    def __init__(self):
        self.states = []  # Estados publicos
        self.state = Adentro()
        self.hidden_state = Adentro()  # Estado actual
        self.count = -1
        self.event_function = self.empty_event_function

    def measure_state(self, distance):
        """Medición con ruido del estado actual"""
        if distance is None:
            return self.state
        else:
            return self.state.transition(distance)

    def update(self, distance):
        # Medimos estado
        new_state = self.measure_state(distance)
        # Si el estado medido coincide solo actualizamos estado oculto
        if new_state == self.state:
            self.hidden_state = new_state
            self.count = -1
        # Si el estado oculto coincide con el anterior aumentamos la cuenta
        elif self.hidden_state == new_state:
            self.count += 1
        # Si no coincide cambiamos el estado oculto y reseteamos el conteo
        else:
            self.hidden_state = new_state
            self.count = 1
        # Si la cuenta alcanza 6 ejecutamos la lógica necesaria,
        # cambiamos estado y reseteamos conteo
        if self.count == 6:
            # Ejecutamos el evento
            output = self.state.transition_function()
            # Actualizamos estado y reseteamos cuenta
            self.state = self.hidden_state
            self.count = -1
            return output
        else:
            output = self.empty_event_function()
            return output
