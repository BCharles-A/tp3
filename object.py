import numpy as np

class Physic:
    def __init__(self, velocity, position, radius, resistance, epsilon, pos_min, pos_max, restitution_coeff):
        self.velocity = velocity
        self.position = position
        self.radius = radius
        self.resistance = resistance
        self.epsilon = epsilon
        self.pos_min = pos_min + np.array([radius, radius])
        self.pos_max = pos_max - np.array([radius, radius])
        self.restitution_coeff = restitution_coeff

    def move(self, time):
        self.velocity = self.velocity * (1 - self.resistance * (time/1000))
        self.position = self.position + self.velocity * (time/1000)
        if np.linalg.norm(self.velocity) < self.epsilon:
            self.velocity = np.array([0, 0])
        if np.any(self.position < self.pos_min):
            if self.position[0] < self.pos_min[0]:
                n = np.array([1, 0])
                self.position[0] = self.pos_min[0]
                self.velocity = self.velocity - (1+self.restitution_coeff) * np.dot(self.velocity, n) * n
            if self.position[1] < self.pos_min[1]:
                n = np.array([0, 1])
                self.position[1] = self.pos_min[1]
                self.velocity = self.velocity - (1+self.restitution_coeff) * np.dot(self.velocity, n) * n
        if np.any(self.position > self.pos_max):
            if self.position[0] > self.pos_max[0]:
                n = np.array([1, 0])
                self.position[0] = self.pos_max[0]
                self.velocity = self.velocity - (1+self.restitution_coeff) * np.dot(self.velocity, n) * n
            if self.position[1] > self.pos_max[1]:
                n = np.array([0, 1])
                self.position[1] = self.pos_max[1]
                self.velocity = self.velocity - (1+self.restitution_coeff) * np.dot(self.velocity, n) * n
            self.velocity = self.velocity * self.restitution_coeff
        return self.position
    
    def set_velocity(self, velocity):
        self.velocity = velocity
    
    def collision(self, other):
        n = self.position - other.position
        if np.linalg.norm(n) < 2*self.radius:
            #Orthogonal projection
            v_n = np.dot(self.velocity-other.velocity, n)/np.dot(n, n) * n
            #Energy transfer
            v_n = (1+self.restitution_coeff)/2 * v_n
            self.velocity = self.velocity - v_n
            other.velocity = other.velocity + v_n

class Object(Physic):
    def __init__(self, velocity, position, radius, resistance, epsilon, name, color, pos_min, pos_max, restitution_coeff):
        super().__init__(velocity, position, radius, resistance, epsilon, pos_min, pos_max, restitution_coeff)
        self.name = name
        self.color = color

    def move(self, time):
        return self.name, super().move(time)