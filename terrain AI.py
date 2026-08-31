import math
import pygame
import moderngl
import numpy as np


# ============================================================
# TERRAIN BACKEND
# ============================================================

class Terrain:
    def __init__(
        self,
        resolution=100,
        size=50.0,
        height_scale=10.0,
        seed=1234,
        octaves=5,
    ):
        self.resolution = resolution
        self.size = size
        self.height_scale = height_scale
        self.seed = seed
        self.octaves = octaves

        self.vertices = None
        self.indices = None
        self.normals = None

        self.min_height = 0
        self.max_height = 0

        self.generate()

    def generate(self):
        heightmap = self.generate_heightmap()

        self.vertices = self.generate_vertices(heightmap)
        self.indices = self.generate_indices()
        self.normals = self.generate_normals()

        self.min_height = float(np.min(self.vertices[:, 1]))
        self.max_height = float(np.max(self.vertices[:, 1]))

    # --------------------------------------------------------
    # Smooth random terrain
    # --------------------------------------------------------

    def generate_heightmap(self):
        """
        Generates smooth random terrain using several layers
        of interpolated random noise.
        """

        rng = np.random.default_rng(self.seed)

        result = np.zeros(
            (self.resolution, self.resolution),
            dtype=np.float32
        )

        amplitude = 1.0
        total_amplitude = 0.0

        for octave in range(self.octaves):

            frequency = 2 ** octave

            # Random values on a low-resolution grid
            lattice = rng.uniform(
                -1.0,
                1.0,
                size=(frequency + 1, frequency + 1)
            )

            x_coords = np.linspace(
                0,
                frequency,
                self.resolution
            )

            z_coords = np.linspace(
                0,
                frequency,
                self.resolution
            )

            x0 = np.floor(x_coords).astype(int)
            z0 = np.floor(z_coords).astype(int)

            # Prevent reading outside the lattice
            x0 = np.minimum(x0, frequency - 1)
            z0 = np.minimum(z0, frequency - 1)

            x1 = x0 + 1
            z1 = z0 + 1

            tx = x_coords - x0
            tz = z_coords - z0

            # Smoothstep interpolation
            tx = tx * tx * (3.0 - 2.0 * tx)
            tz = tz * tz * (3.0 - 2.0 * tz)

            v00 = lattice[
                z0[:, None],
                x0[None, :]
            ]

            v10 = lattice[
                z0[:, None],
                x1[None, :]
            ]

            v01 = lattice[
                z1[:, None],
                x0[None, :]
            ]

            v11 = lattice[
                z1[:, None],
                x1[None, :]
            ]

            tx_grid = tx[None, :]
            tz_grid = tz[:, None]

            top = v00 * (1.0 - tx_grid) + v10 * tx_grid
            bottom = v01 * (1.0 - tx_grid) + v11 * tx_grid

            noise = top * (1.0 - tz_grid) + bottom * tz_grid

            result += noise * amplitude

            total_amplitude += amplitude
            amplitude *= 0.5

        result /= total_amplitude

        result *= self.height_scale

        return result.astype(np.float32)

    # --------------------------------------------------------
    # Turn heightmap into XYZ points
    # --------------------------------------------------------

    def generate_vertices(self, heightmap):
        vertices = []

        half_size = self.size / 2.0

        for z in range(self.resolution):
            for x in range(self.resolution):

                world_x = (
                    x / (self.resolution - 1)
                ) * self.size - half_size

                world_z = (
                    z / (self.resolution - 1)
                ) * self.size - half_size

                world_y = heightmap[z, x]

                vertices.append([
                    world_x,
                    world_y,
                    world_z
                ])

        return np.array(vertices, dtype=np.float32)

    # --------------------------------------------------------
    # Connect points into triangles
    # --------------------------------------------------------

    def generate_indices(self):
        indices = []

        for z in range(self.resolution - 1):
            for x in range(self.resolution - 1):

                top_left = (
                    z * self.resolution + x
                )

                top_right = top_left + 1

                bottom_left = (
                    (z + 1) * self.resolution + x
                )

                bottom_right = bottom_left + 1

                # Triangle 1
                indices.extend([
                    top_left,
                    bottom_left,
                    top_right
                ])

                # Triangle 2
                indices.extend([
                    top_right,
                    bottom_left,
                    bottom_right
                ])

        return np.array(indices, dtype=np.uint32)

    # --------------------------------------------------------
    # Calculate normals for lighting
    # --------------------------------------------------------

    def generate_normals(self):
        normals = np.zeros_like(self.vertices)

        triangles = self.indices.reshape(-1, 3)

        v0 = self.vertices[triangles[:, 0]]
        v1 = self.vertices[triangles[:, 1]]
        v2 = self.vertices[triangles[:, 2]]

        edge1 = v1 - v0
        edge2 = v2 - v0

        triangle_normals = np.cross(edge1, edge2)

        lengths = np.linalg.norm(
            triangle_normals,
            axis=1,
            keepdims=True
        )

        lengths[lengths == 0] = 1.0

        triangle_normals /= lengths

        np.add.at(
            normals,
            triangles[:, 0],
            triangle_normals
        )

        np.add.at(
            normals,
            triangles[:, 1],
            triangle_normals
        )

        np.add.at(
            normals,
            triangles[:, 2],
            triangle_normals
        )

        lengths = np.linalg.norm(
            normals,
            axis=1,
            keepdims=True
        )

        lengths[lengths == 0] = 1.0

        normals /= lengths

        return normals.astype(np.float32)


# ============================================================
# CAMERA
# ============================================================

class OrbitCamera:
    def __init__(self):
        self.target = np.array(
            [0.0, 0.0, 0.0],
            dtype=np.float32
        )

        self.distance = 70.0

        self.yaw = math.radians(45)
        self.pitch = math.radians(35)

    def get_position(self):
        x = (
            math.cos(self.pitch)
            * math.cos(self.yaw)
            * self.distance
        )

        y = (
            math.sin(self.pitch)
            * self.distance
        )

        z = (
            math.cos(self.pitch)
            * math.sin(self.yaw)
            * self.distance
        )

        return self.target + np.array(
            [x, y, z],
            dtype=np.float32
        )

    def rotate(self, dx, dy):
        sensitivity = 0.005

        self.yaw += dx * sensitivity
        self.pitch -= dy * sensitivity

        self.pitch = max(
            math.radians(5),
            min(
                math.radians(85),
                self.pitch
            )
        )

    def zoom(self, amount):
        self.distance *= 0.9 ** amount

        self.distance = max(
            10.0,
            min(200.0, self.distance)
        )


# ============================================================
# MATRIX FUNCTIONS
# ============================================================

def normalize(vector):
    length = np.linalg.norm(vector)

    if length == 0:
        return vector

    return vector / length


def look_at(eye, target, up):
    forward = normalize(target - eye)

    right = normalize(
        np.cross(forward, up)
    )

    camera_up = np.cross(
        right,
        forward
    )

    matrix = np.array([
        [
            right[0],
            right[1],
            right[2],
            -np.dot(right, eye)
        ],
        [
            camera_up[0],
            camera_up[1],
            camera_up[2],
            -np.dot(camera_up, eye)
        ],
        [
            -forward[0],
            -forward[1],
            -forward[2],
            np.dot(forward, eye)
        ],
        [
            0,
            0,
            0,
            1
        ]
    ], dtype=np.float32)

    return matrix


def perspective(
    fov_degrees,
    aspect,
    near,
    far
):
    fov = math.radians(fov_degrees)

    f = 1.0 / math.tan(fov / 2.0)

    matrix = np.zeros(
        (4, 4),
        dtype=np.float32
    )

    matrix[0, 0] = f / aspect
    matrix[1, 1] = f

    matrix[2, 2] = (
        (far + near)
        / (near - far)
    )

    matrix[2, 3] = (
        (2.0 * far * near)
        / (near - far)
    )

    matrix[3, 2] = -1.0

    return matrix


# ============================================================
# RENDERER / FRONTEND
# ============================================================

class TerrainApp:
    def __init__(self):
        pygame.init()

        self.width = 1280
        self.height = 720

        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_MAJOR_VERSION,
            3
        )

        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_MINOR_VERSION,
            3
        )

        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK,
            pygame.GL_CONTEXT_PROFILE_CORE
        )

        pygame.display.set_mode(
            (self.width, self.height),
            pygame.OPENGL
            | pygame.DOUBLEBUF
            | pygame.RESIZABLE
        )

        pygame.display.set_caption(
            "Python Terrain Renderer"
        )

        self.ctx = moderngl.create_context()

        self.ctx.enable(
            moderngl.DEPTH_TEST
        )

        self.clock = pygame.time.Clock()

        self.camera = OrbitCamera()

        self.wireframe = False
        self.dragging = False

        self.seed = 1234

        self.terrain = Terrain(
            resolution=120,
            size=60,
            height_scale=12,
            seed=self.seed,
            octaves=6
        )

        self.create_shader()
        self.create_mesh()

    # --------------------------------------------------------
    # Shader
    # --------------------------------------------------------

    def create_shader(self):
        self.program = self.ctx.program(

            vertex_shader="""
                #version 330

                uniform mat4 mvp;

                in vec3 in_position;
                in vec3 in_normal;

                out vec3 normal;
                out float height;

                void main()
                {
                    gl_Position =
                        mvp * vec4(in_position, 1.0);

                    normal = in_normal;
                    height = in_position.y;
                }
            """,

            fragment_shader="""
                #version 330

                in vec3 normal;
                in float height;

                uniform float min_height;
                uniform float max_height;

                out vec4 fragColor;

                void main()
                {
                    vec3 n = normalize(normal);

                    vec3 lightDirection =
                        normalize(vec3(
                            0.5,
                            1.0,
                            0.3
                        ));

                    float diffuse =
                        max(
                            dot(
                                n,
                                lightDirection
                            ),
                            0.0
                        );

                    float lighting =
                        0.30
                        + diffuse * 0.70;

                    float range =
                        max_height
                        - min_height;

                    float t =
                        (height - min_height)
                        / max(range, 0.001);

                    vec3 lowColor =
                        vec3(
                            0.12,
                            0.35,
                            0.12
                        );

                    vec3 middleColor =
                        vec3(
                            0.35,
                            0.28,
                            0.15
                        );

                    vec3 highColor =
                        vec3(
                            0.75,
                            0.75,
                            0.72
                        );

                    vec3 color;

                    if (t < 0.55)
                    {
                        color = mix(
                            lowColor,
                            middleColor,
                            t / 0.55
                        );
                    }
                    else
                    {
                        color = mix(
                            middleColor,
                            highColor,
                            (t - 0.55) / 0.45
                        );
                    }

                    color *= lighting;

                    fragColor =
                        vec4(color, 1.0);
                }
            """
        )

    # --------------------------------------------------------
    # Upload terrain to GPU
    # --------------------------------------------------------

    def create_mesh(self):
        if hasattr(self, "vao"):
            self.vao.release()
            self.vbo.release()
            self.ibo.release()

        combined = np.hstack([
            self.terrain.vertices,
            self.terrain.normals
        ]).astype(np.float32)

        self.vbo = self.ctx.buffer(
            combined.tobytes()
        )

        self.ibo = self.ctx.buffer(
            self.terrain.indices.tobytes()
        )

        self.vao = self.ctx.vertex_array(
            self.program,
            [
                (
                    self.vbo,
                    "3f 3f",
                    "in_position",
                    "in_normal"
                )
            ],
            self.ibo
        )

    # --------------------------------------------------------
    # Regenerate terrain
    # --------------------------------------------------------

    def regenerate(self):
        self.seed += 1

        self.terrain = Terrain(
            resolution=120,
            size=60,
            height_scale=12,
            seed=self.seed,
            octaves=6
        )

        self.create_mesh()

    # --------------------------------------------------------
    # Input
    # --------------------------------------------------------

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.VIDEORESIZE:
                self.width = event.w
                self.height = event.h

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return False

                if event.key == pygame.K_w:
                    self.wireframe = not self.wireframe

                if event.key == pygame.K_r:
                    self.regenerate()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    self.dragging = True

            if event.type == pygame.MOUSEBUTTONUP:

                if event.button == 1:
                    self.dragging = False

            if event.type == pygame.MOUSEMOTION:

                if self.dragging:
                    dx, dy = event.rel

                    self.camera.rotate(
                        dx,
                        dy
                    )

            if event.type == pygame.MOUSEWHEEL:
                self.camera.zoom(
                    event.y
                )

        return True

    # --------------------------------------------------------
    # Render
    # --------------------------------------------------------

    def render(self):
        self.ctx.viewport = (
            0,
            0,
            self.width,
            self.height
        )

        self.ctx.clear(
            0.07,
            0.09,
            0.12
        )

        eye = self.camera.get_position()

        view = look_at(
            eye,
            self.camera.target,
            np.array(
                [0, 1, 0],
                dtype=np.float32
            )
        )

        aspect = (
            self.width
            / max(self.height, 1)
        )

        projection = perspective(
            60.0,
            aspect,
            0.1,
            500.0
        )

        mvp = projection @ view

        # GLSL uses column-major matrices
        self.program["mvp"].write(
            mvp.T
            .astype("f4")
            .tobytes()
        )

        self.program[
            "min_height"
        ].value = self.terrain.min_height

        self.program[
            "max_height"
        ].value = self.terrain.max_height

        self.ctx.wireframe = self.wireframe

        self.vao.render(
            moderngl.TRIANGLES
        )

        pygame.display.flip()

    # --------------------------------------------------------
    # Main loop
    # --------------------------------------------------------

    def run(self):
        running = True

        while running:

            running = self.handle_events()

            self.render()

            self.clock.tick(60)

        self.destroy()

    def destroy(self):
        self.vao.release()
        self.vbo.release()
        self.ibo.release()
        self.program.release()

        pygame.quit()


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    app = TerrainApp()
    app.run()