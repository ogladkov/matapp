import bpy


{{MAT_DATA}}

# Open blender file (with materials)
scene_file_path = "./data/METERIAL_METALICO.blend"
bpy.ops.wm.open_mainfile(filepath=scene_file_path)

gltf_fpath = './data/output/model.glb'

# Specify the name of the target collection
target_collection_name = 'ImportedGLTFObjects'

# Step 1: Import the glTF file
bpy.ops.import_scene.gltf(filepath=gltf_fpath)

# Step 2: Move the imported objects to the specified collection
# First, find or create the target collection
if target_collection_name not in bpy.data.collections:
    target_collection = bpy.data.collections.new(name=target_collection_name)
    bpy.context.scene.collection.children.link(target_collection)
else:
    target_collection = bpy.data.collections[target_collection_name]

# Identify the imported objects (assuming they are the only newly added objects)
imported_objects = [obj for obj in bpy.context.scene.objects if obj.select_get()]

# Move each imported object to the target collection
for obj in imported_objects:
    # Unlink from all current collections
    for col in obj.users_collection:
        col.objects.unlink(obj)
    # Link to the target collection
    target_collection.objects.link(obj)

# Step 3: Iterate through the objects in the specified collection
for obj in target_collection.objects:

    if obj.type == 'MESH':
        # Example operation: Print the name of each object
        print(f"Object name: {obj.data.name}")
        # Add any additional operations you want to perform on each object here

        if '_x_stone' in obj.data.name:
            correct_mat = mat_data['stone']

        elif '_x_metal' in obj.data.name:
            correct_mat = mat_data['metal']

        else:
            print(f'ERRROR: no material label for {obj.name}!')


        obj.data.materials.clear()
        obj_mat = bpy.data.materials.get(correct_mat)
        obj.data.materials.append(obj_mat)

# Save the scene as glTF
bpy.ops.export_scene.gltf(
    filepath=f'./data/output/model.glb',
    export_format='GLB'
)
