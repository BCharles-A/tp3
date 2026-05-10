import numpy as np

class Physic:
    def __init__(self, velocity, position, radius, resistance, epsilon, pos_min, pos_max):
        self.velocity = velocity
        self.position = position
        self.radius = radius
        self.resistance = resistance
        self.epsilon = epsilon
        self.pos_min = pos_min
        self.pos_max = pos_max

    def move(self, time):
        self.position = self.position + self.velocity
        self.velocity = self.velocity * (1 - self.resistance * (time/1000))
        if np.linalg.norm(self.velocity) < self.epsilon:
            self.velocity = np.array([0, 0])
        if np.any(self.position < self.pos_min):
            if self.position[0] < self.pos_min[0]:
                self.position[0] = self.pos_min[0]
                self.velocity[0] = -self.velocity[0]
            elif self.position[1] < self.pos_min[1]:
                self.position[1] = self.pos_min[1]
                self.velocity[1] = -self.velocity[1]
        elif np.any(self.position > self.pos_max):
            if self.position[0] > self.pos_max[0]:
                self.position[0] = self.pos_max[0]
                self.velocity[0] = -self.velocity[0]
            elif self.position[1] > self.pos_max[1]:
                self.position[1] = self.pos_max[1]
                self.velocity[1] = -self.velocity[1]
        return self.position
    
    def set_velocity(self, velocity):
        self.velocity = velocity
    
    def collision(self, other):
        pass


class Object(Physic):
    def __init__(self, velocity, position, radius, resistance, epsilon, name, color, pos_min, pos_max):
        super().__init__(velocity, position, radius, resistance, epsilon, pos_min, pos_max)
        self.name = name
        self.color = color

    def move(self, time):
        return self.name, super().move(time)