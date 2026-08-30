import pygame
import moderngl


pygame.init()

width = 1280
height = 720

pygame.display.set_mode(
    (width, height),
    pygame.OPENGL | pygame.DOUBLEBUF
)

ctx = moderngl.create_context()

ctx.enable(moderngl.DEPTH_TEST)

clock = pygame.time.Clock()

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    ctx.clear(0.1, 0.1, 0.1)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()