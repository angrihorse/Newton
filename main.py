from pygame.locals import *
import pygame
import sys
import numpy as np
import newton


# Set simulation parameters.
window_size = [800, 600]
bg_color = (255,255,255)
gravity = [0, 0]
friction = 0
dt = 0.01
number_of_balls = 20

# Initialize the environment.
env = newton.Environment(window_size, gravity, friction, dt)
pygame.init()
pygame.display.set_caption('Matrix')
screen = pygame.display.set_mode((window_size[0], window_size[1]))

def generate_balls(number_of_balls):
    for ball in range(number_of_balls):
        speed = [np.random.randint(-600, 600), np.random.randint(-600, 600)]
        acceleration = [0, 0]
        radius = np.random.randint(20, 40)
        coordinates = [np.random.randint(radius, window_size[0]-radius), np.random.randint(radius, window_size[1]-radius)]
        mass = np.random.randint(40, 60)
        color = (0, 0, 0)
        env.add_object(newton.Ball(env, coordinates, speed, acceleration, radius, mass, color))

def draw_env(env):
    screen.fill(bg_color)
    for i in env.objects:
        pygame.draw.circle(screen, i.color, (int(i.x), int(i.y)), i.radius, 1)
    pygame.display.flip()

# Run the simulation.
clock = pygame.time.Clock()
generate_balls(number_of_balls)
while True:
    clock.tick(60)
    env.update()
    draw_env(env)

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
