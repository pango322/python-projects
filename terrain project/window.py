import pygame
import moderngl
from altitude_generator import * #simply using import altitude_generator is enough but i prefer not using namespaces even if its more confusing
from helpers import * #same as above

screenx = 800
screeny = 600
pygame.init()

screen = pygame.display.set_mode((screenx, screeny), pygame.OPENGL | pygame.DOUBLEBUF) #start an opengl capable window with doublebuff meaning 2x the render

ctx = moderngl.create_context() #create a moderngl context this is our interface to the GPU
ctx.enable(moderngl.DEPTH_TEST) #enable depth testing so that closer objects are drawn in front of farther ones avoids drawing objects that are behind other objects

vbo = ctx.buffer(vertices.tobytes()) #sends data to the GPU
ibo = ctx.buffer(indices.tobytes()) 

program = ctx.program( #stole this shader it should be simple just makes sure the color of the mesh is based on the height of the vertex
    vertex_shader="""
        #version 330

        uniform mat4 mvp;

        in vec3 position;
        out float height;

        void main() {
            height = position.y;
            gl_Position = mvp * vec4(position, 1.0);
        }
    """,

    fragment_shader="""
        #version 330

        in float height;
        out vec4 color;

        void main() {

            if (height < -1.0)
                color = vec4(0.1, 0.4, 0.1, 1.0);

            else if (height < 2.0)
                color = vec4(0.4, 0.3, 0.1, 1.0);

            else
                color = vec4(0.8, 0.8, 0.8, 1.0);
        }
    """
)

vao = ctx.vertex_array(program, [(vbo, '3f', 'position')], ibo) #tells the GPU how to interpret the data we sent it connects the shader to the data

eye = np.array([40, 10, 20], dtype="f4") #camera position
target = np.array([0, 0, 0], dtype="f4") #target position

view = look_at(eye, target) #creates a view matrix that will be used to transform the vertices from world space to camera space
projection = perspective(45.0, screenx / screeny, 0.1, 100.0) #creates a projection matrix that will be used to transform the vertices from camera space to clip space
mvp = projection @ view #creates a model-view-projection matrix that will be used to transform the vertices from world space to clip space
program['mvp'].write(mvp.T.astype('f4').tobytes()) #sends the model-view-projection matrix to the GPU so that it can be used in the vertex shader



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        vao.render(moderngl.TRIANGLES) #this is the part that actually draws the mesh to the screen

        ctx.clear(0.1, 0.1, 0.1) #clear the screen with a dark gray color
        vao.render(moderngl.TRIANGLES)
        pygame.display.flip() #swap the front and back buffers to display the rendered image

pygame.quit()