import pygame
import moderngl

pygame.init()

width = 1280
height = 720

pygame.display.set_mode(
    (width, height),
    pygame.OPENGL | pygame.DOUBLEBUF
) #doublebuff doubles the number of drawings to prevent tearing

ctx = moderngl.create_context() #automatically creates a context for moderngl to use, which is a wrapper for OpenGL connecting to the GPU

ctx.enable(moderngl.DEPTH_TEST) #avoid rendering objects that are behind other objects

clock = pygame.time.Clock() #gives us control of the framerate of the program, so it doesn't run too fast or too slow

running = True

while running:

    for event in pygame.event.get(): #go through all the different pygame events that have happened since the last time this loop ran

        if event.type == pygame.QUIT:
            running = False

    ctx.clear(0.1, 0.1, 0.1)

    pygame.display.flip()

    clock.tick(60) #limits the framerate to 60 frames per second

pygame.quit()