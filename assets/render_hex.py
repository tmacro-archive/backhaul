#!/usr/bin/python3

import bpy
from math import pi
import bmesh
from mathutils import Vector
from PIL import Image

def remove_cube():
	if "Cube" in bpy.data.meshes:
		mesh = bpy.data.meshes["Cube"]
		print("removing mesh", mesh)
		bpy.data.meshes.remove(mesh, do_unlink=True)

def remove_lamp():
	bpt.data.lamps.remove('Lamp', do_unlink=True)

def get_camera():
	return bpy.data.cameras['Camera']\

def setup_camera(camera, tx = 5.0, ty = 0.0, tz = 3.9, 
					rx = 60.0, ry = 0.0, rz = 90.0, fov = 50.0):
	camera.data.type = 'ORTHO'
	camera.data.ortho_scale = 4.3
	# camera.data.angle = fov*(pi/180.0)

	# Set camera rotation in euler angles
	camera.rotation_mode = 'XYZ'
	camera.rotation_euler[0] = rx*(pi/180.0)
	camera.rotation_euler[1] = ry*(pi/180.0)
	camera.rotation_euler[2] = rz*(pi/180.0)

	# Set camera translation
	camera.location.x = tx
	camera.location.y = ty
	camera.location.z = tz

def setup_light():
	scene = bpy.context.scene
	# Create new lamp datablock
	lamp_data = bpy.data.lamps.new(name="New Lamp", type='POINT')
	# Create new object with our lamp datablock
	lamp_object = bpy.data.objects.new(name="New Lamp", object_data=lamp_data)
	# Link lamp object to the scene so it'll appear in this scene
	scene.objects.link(lamp_object)
	# Place lamp to a specified location
	lamp_object.location = (5.0, 0.0, 3.0)
	# And finally select it make active
	lamp_object.select = True
	scene.objects.active = lamp_object

def makeMaterial(name, diffuse, specular, alpha):
	mat = bpy.data.materials.new(name)
	mat.diffuse_color = diffuse
	mat.diffuse_shader = 'LAMBERT' 
	mat.diffuse_intensity = 1.0 
	mat.specular_color = specular
	mat.specular_shader = 'COOKTORR'
	mat.specular_intensity = 0.5
	mat.alpha = alpha
	mat.ambient = 1
	# img = bpy.data.images.load('dirt.png')
	# cTex = bpy.data.textures.new('ColorTex', type = 'IMAGE')
	# cTex.image = img
	# # Create material
	# mat = bpy.data.materials.new('TexMat')
	# # Add texture slot for color texture
	# mtex = mat.texture_slots.add()
	# mtex.texture = cTex
	return mat
 
def setMaterial(ob, mat):
	me = ob.data
	me.materials.append(mat)

def create_hex(r, g, b):
	bpy.ops.mesh.primitive_circle_add(vertices=6, radius=2.1, fill_type='NGON', 
										location=(0, 0, 0), rotation=(0, 0, 0))

	ob = bpy.context.object
	me = ob.data

	bm = bmesh.new()
	bm.from_mesh(me)
	faces = bm.faces[:]

	for face in faces:
		q = bmesh.ops.extrude_discrete_faces(bm, faces=[face])
		bmesh.ops.translate(bm, vec=Vector((0,0,2.1)), verts=q['faces'][0].verts)

	bm.to_mesh(me)
	me.update()
	red = makeMaterial('Magic', (r/255.0, g/255.0, b/255.0), (0,0,0), 1)
	setMaterial(ob, red)

def render_tile():
	scene = bpy.context.scene
	fp = '/home/tmac/proj/public/backhaul/assets/' # get existing output path
	scene.render.image_settings.file_format = 'PNG' # set output format to .png

	scene.frame_set(0)

	# set output path so render won't get overwritten
	scene.render.filepath = fp + 'tile.png'
	bpy.ops.render.render(write_still=True) # render still

	# restore the filepath
	scene.render.filepath = fp

def autocrop_image(image, border = 0):
	# Get the bounding box
	bbox = image.getbbox()
 
	# Crop the image to the contents of the bounding box
	image = image.crop(bbox)
 
	# Determine the width and height of the cropped image
	(width, height) = image.size
 
	# Add border
	width += border * 2
	height += border * 2
 
	# Create a new image object for the output image
	cropped_image = Image.new("RGBA", (width, height), (0,0,0,0))
 
	# Paste the cropped image onto the new image
	cropped_image.paste(image, (border, border))
 
	# Done!
	return cropped_image

scene = bpy.data.scenes["Scene"]
# Set render resolution
scene.render.resolution_x = 128
scene.render.resolution_y = 128
# scene.render.use_antialiasing = False
scene.render.alpha_mode = 'TRANSPARENT'
# Set camera fov in degrees

setup_camera(scene.camera)
setup_light()
remove_cube()

create_hex(74, 50, 29)

# img = bpy.data.images.load('dirt.png')
# cTex = bpy.data.textures.new('ColorTex', type = 'IMAGE')
# cTex.image = img
# # Create material
# mat = bpy.data.materials.new('TexMat')

# # Add texture slot for color texture
# mtex = mat.texture_slots.add()
# mtex.texture = cTex
# # Add material to current object
# ob = bpy.context.object
# me = ob.data
# me.materials.append(mat)
render_tile()
image = Image.open('/home/tmac/proj/public/backhaul/assets/tile.png')
image = autocrop_image(image, border = -1)
image.save('/home/tmac/proj/public/backhaul/assets/tile.png')