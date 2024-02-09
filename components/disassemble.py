import bpy
import os
from pathlib import Path
import time

# save_off_dir = Path('/home/sm00th/Downloads/test_matapp/data/input/off/')
save_off_dir = Path('./data/input/off/')
# save_usd_dir = Path('/home/sm00th/Downloads/test_matapp/data/input/parts')  # Directory to save separated USD files
save_usd_dir = Path('./data/input/parts')  # Directory to save separated USD files

# folder_path = Path("/home/sm00th/Downloads/test_matapp/data/input")
folder_path = Path("./data/input")
# usd_file = Path("/home/sm00th/Downloads/test_matapp/data/input/model.usd")
usd_file = Path("./data/input/model.usd")

# Create the full path to the USD file
usd_file_path = os.path.join(folder_path, 'model.usd')

# Clear existing mesh objects in the scene
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Clear existing objects in the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import USD file
bpy.ops.wm.usd_import(filepath=str(usd_file))

# Process each object in the scene
for obj in bpy.data.objects:
    bpy.ops.object.select_all(action='DESELECT')

    if obj.type == 'MESH':
        # Select the object
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        # Export the current object as a separate USD file
        # usd_filename = f"{usd_file.stem}_{obj.name}.usdc"
        # usd_fpath = save_usd_dir / usd_filename
        # mesh_obj = bpy.data.objects.get(obj.name)
        # mesh_obj.select_set(True)
        # bpy.context.view_layer.objects.active = mesh_obj
        # bpy.ops.wm.usd_export(filepath=str(usd_fpath), selected_objects_only=True)

        # print(f"{obj.name} saved as separate USD file at {usd_fpath}")

        # Switch to Object mode (if not already)
        bpy.ops.object.mode_set(mode='OBJECT')

        # Create a list to store vertex coordinates (not using set to maintain order)
        vertex_coordinates = []

        # Iterate through vertices and store their coordinates
        for vertex in obj.data.vertices:
            # Convert vertex coordinate tuple to a string
            coord_str = f"{vertex.co.x} {vertex.co.y} {vertex.co.z}"
            vertex_coordinates.append(coord_str)

        # Create a list to store faces
        faces = []

        # Iterate through the faces and store the indices of their vertices
        for face in obj.data.polygons:
            face_indices = [str(vertex_index) for vertex_index in face.vertices]
            faces.append(" ".join(face_indices))

        # Write vertex coordinates and faces to a text file
        filename = f"{usd_file.stem}_{obj.name}.off"
        fpath = save_off_dir / filename

        with open(fpath, 'w') as file:
            file.write("OFF\n")
            file.write(f"{len(vertex_coordinates)} {len(faces)} 0\n")  # Number of vertices and faces

            for vertex_coord in vertex_coordinates:
                file.write(f"{vertex_coord}\n")

            for face in faces:
                file.write(f"3 {face}\n")  # Assuming all faces are triangles

        # Deselect the object after processing
        obj.select_set(False)
