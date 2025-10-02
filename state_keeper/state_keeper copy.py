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
    def transition(self, distance):
        if distance >= -150:
            return Calle()
        else:
            return self

    def __str__(self):
        return "Adentro"


class Calle(State):
    def transition(self, distance):
        if distance > 150.:
            return Afuera()
        elif distance < -150:
            return Adentro()
        else:
            return self

    def __str__(self):
        return "Calle"


class Afuera(State):
    def transition(self, distance):
        if distance <= 150:
            return Calle()
        else:
            return self

    def __str__(self):
        return "Afuera"


class StateKeeper:
    def __init__(self):
        self.states = []  # Estados publicos
        self.state = Adentro()
        self.hidden_state = Adentro()  # Estado actual
        self.count = -1

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
            return
        # Si el estado oculto coincide con el anterior aumentamos la cuenta
        if self.hidden_state == new_state:
            self.count += 1
        # Si no cambiamos el estado oculto y reseteamos el conteo
        else:
            self.hidden_state = new_state
            self.count = 1
        # Si la cuenta alcanza 10 cambiamos estado y reseteamos conteo
        if self.count == 6:
            self.state = self.hidden_state
            self.count = -1
