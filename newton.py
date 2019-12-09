import numpy as np


class Environment:
    def __init__(self, window_size, gravity, dampening, dt):
        self.window_size = window_size
        self.gravity = gravity
        self.dampening = dampening
        self.dt = dt
        self.objects = []

    def update(self):
        for i in self.objects:
            self.bounce_of_walls(i)
            for j in self.objects:
                if i != j: self.collide(i, j)
            i.accelerate(*self.gravity)
            i.move()

    def bounce_of_walls(self, i):
        if i.y - i.radius <= 0:
            i.dy *= -1
            i.y = i.radius
        if i.y + i.radius >= self.window_size[1]:
            i.dy *= -1
            i.y = self.window_size[1] - i.radius
        if i.x - i.radius <= 0:
            i.dx *= -1
            i.x = i.radius
        if i.x + i.radius >= self.window_size[0]:
            i.dx *= -1
            i.x = self.window_size[0] - i.radius

    def collide(self, i, j):
        X, Y = i.x - j.x, i.y - j.y
        distance = np.sqrt((X**2)+(Y**2))
        penetration_depth = i.radius + j.radius - distance
        if penetration_depth >= 0:
            # Reference: http://www.vobarian.com/collisions/2dcollisions2.pdf.
            n = np.asarray([X, Y])/distance # Normal unit vector.
            t = np.asarray([-n[1], n[0]]) # Tangential unit vector.

            # Set initial velocity vectors.
            v1 = np.asarray([i.dx, i.dy])
            v2 = np.asarray([j.dx, j.dy])

            # Project the velocity vectors onto
            # the unit normal and unit tangent vectors
            v1n = np.dot(n, v1)
            v1t = np.dot(t, v1)
            v2n = np.dot(n, v2)
            v2t = np.dot(t, v2)

            # Find tangential velocities after the collision.
            u1t = v1t
            u2t = v2t

            # Find the new normal velocities.
            m1, m2 = i.mass, j.mass
            M1, M2 = m1 + m2, m1 - m2
            u1n = (v1n*M2+2*m2*v2n)/M1
            u2n = (-v2n*M2+2*m1*v1n)/M1

            # Convert the scalar normal and
            # tangential velocities into vectors.
            u1n *= n
            u1t *= t
            u2n *= n
            u2t *= t

            # Find the final velocity vectors.
            u1 = u1n + u1t
            u2 = u2n + u2t

            # Set the final velocity vectors.
            i.dx, i.dy = self.dampening * u1
            j.dx, j.dy = self.dampening * u2

            # Percent of correction and threshold above which positional cprrection is not preformed.
            percent, threshold = 0.2, 1
            correction = percent * max(0, penetration_depth - threshold)

            # Move objects away from each other to avoid sinking.
            i.x += correction * n[0]
            i.y += correction * n[1]
            j.x -= correction * n[0]
            j.y -= correction * n[1]


class Ball:
    def __init__(self, env, coordinates, velocity, radius, mass):
        self.env = env
        self.x, self.y = coordinates
        self.dx, self.dy = velocity
        self.radius = radius
        self.mass = mass

    def accelerate(self, dax, day):
        self.dx += dax * self.env.dt
        self.dy += day * self.env.dt

    def move(self):
        self.x += self.dx
        self.y += self.dy
