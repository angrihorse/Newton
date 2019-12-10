from pygame.locals import *
import pygame
import sys
import numpy as np
import newton


# Set simulation parameters.
window_size = [1080, 720]
gravity = [0, 5]
dampening = 0.95
bg_color = (33, 33, 33)
ball_color = (255, 235, 59)
fps = 60
dt = 1/fps
number_of_balls = 64

# Initialize the environment.
env = newton.Environment(window_size, gravity, dampening, dt)
pygame.init()
pygame.display.set_caption('Collision simulation')
screen = pygame.display.set_mode((window_size[0], window_size[1]))

def generate_balls(number_of_balls):
    for ball in range(number_of_balls):
        radius = np.random.randint(15, 30)
        coordinates = np.random.randint(radius, np.array(window_size) - radius, 2)
        velocity = np.random.randint(-20, 20, 2)
        mass = np.random.randint(40, 60)
        env.objects.append((newton.Ball(env, coordinates, velocity, radius, mass)))

def draw_env(env):
    screen.fill(bg_color)
    for i in env.objects:
        pygame.draw.circle(screen, ball_color, (int(i.x), int(i.y)), i.radius, 1)
    pygame.display.flip()

# Run the simulation.
clock = pygame.time.Clock()
generate_balls(number_of_balls)
while True:
    clock.tick(fps)
    env.update()
    draw_env(env)

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
