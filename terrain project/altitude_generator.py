import numpy as np

resolution = 100

heightmap = np.random.uniform(low=-5, high=5.0, size=(resolution, resolution)) #this is a purely random heightmap and will look horrible

x = np.linspace(0, 6, resolution) #evenly spaced set of points from 0 to 6 with a total of resolution points
y = np.linspace(0, 6, resolution)
xv, yv = np.meshgrid(x, y) #a grid of x and y values that will be used to create a more interesting heightmap
heightmap = np.sin(xv) * np.cos(yv) * 5.0 #this is a more interesting heightmap that will look like rolling hills since its just sin and cosine

#now we need to convert the heightmap into xyz points centered around the origin so that we can use it to create a 3D mesh

vertices = []
for z in range(resolution):
    for x in range(resolution):
        y = heightmap[z][x]
        #vertices.append((x, y, z)) #this is the original version that will create a mesh that is not centered around the origin
        vertices.append((x - resolution / 2, y, z - resolution / 2)) #this is the new version that will create a mesh that is centered around the origin
vertices = np.array(vertices, dtype='f4') #convert to numpy array of float32

#we need to split up the squares into triangles since thats how a computer generates 3D meshes
indices = []
for z in range(resolution - 1):
    for x in range(resolution - 1):
        top_left = z * resolution + x
        top_right = top_left + 1
        bottom_left = top_left + resolution
        bottom_right = bottom_left + 1

        indices.append((top_left, bottom_left, top_right))
        indices.append((top_right, bottom_left, bottom_right))
indices = np.array(indices, dtype='u4') #convert to numpy array of uint32