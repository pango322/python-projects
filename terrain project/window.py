import pygame
import moderngl
from altitude_generator import * #simply using import altitude_generator is enough but i prefer not using namespaces even if its more confusing

screenx = 800
screeny = 600
pygame.init()

screen = pygame.display.set_mode((screenx, screeny), pygame.OPENGL | pygame.DOUBLEBUF) #start an opengl capable window with doublebuff meaning 2x the render

ctx = moderngl.create_context() #create a moderngl context this is our interface to the GPU
ctx.enable(moderngl.DEPTH_TEST) #enable depth testing so that closer objects are drawn in front of farther ones avoids drawing objects that are behind other objects

vbo = ctx.buffer(vertices.tobytes()) #sends data to the GPU
ibo = ctx.buffer(indices.tobytes()) 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ctx.clear(0.1, 0.1, 0.1) #clear the screen with a dark gray color
    pygame.display.flip() #swap the front and back buffers to display the rendered image

pygame.quit()