import bpy
import os

{{MAT_DATA}}

# Open blender file (with materials)
scene_file_path = "./data/METERIAL_METALICO.blend"
bpy.ops.wm.open_mainfile(filepath=scene_file_path)

# Apply script
folder_path = "./data/input"

# # Get a list of all files in the folder
# usd_files = [f for f in os.listdir(folder_path) if f.endswith(".usd")]
#
# # Loop through each USD file in the folder
# for usd_file in usd_files:

# Create the full path to the USD file
usd_file_path = os.path.join(folder_path, 'model.usd')
file_prefix = usd_file_path.split('/')[-1].split('.')[0]

# Clear existing mesh objects in the scene
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Import the USD file using the integrated USD import operator
bpy.ops.wm.usd_import(filepath=usd_file_path)

# Select all objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')

# Apply the material to selected objects
for obj in bpy.context.selected_objects:

    if obj.type == 'MESH':
        obj.data.materials.clear()
        obj_mat = bpy.data.materials.get(mat_data[obj.name])
        obj.data.materials.append(obj_mat)

# Save the scene as glTF
bpy.ops.export_scene.gltf(
    filepath=f'./data/output/{file_prefix}.glb',
    export_format='GLB'
)
