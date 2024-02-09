import os
from pathlib import Path
import shutil
import subprocess

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

from components.pcd_sampler import off2pcd
from components.pointnet2.pointnet2_cls import infer


# Start app
app = FastAPI()


@app.post('/simple_apply/')
def simple_apply(mat_id: str, data: UploadFile = File(...)):
    # Save usd
    model_bytes = data.file.read()
    model_path = './data/input/model.usd'

    with open(model_path, 'wb') as model_file:
        model_file.write(model_bytes)

    # Prepare apply_mat.py
    with open('components/apply_mat.py', 'r') as apply_mat:
        apply_mat = apply_mat.read()
        apply_mat = apply_mat.replace('{{MAT}}', f'"{mat_id}"')

    with open('./apply_mat_exec.py', 'w') as apply_mat_exec:
        apply_mat_exec.write(apply_mat)

    # Process model with Blender
    shell_script_path = './components/apply_mat.sh'
    subprocess.run(['sh', shell_script_path])


@app.post('/cls_apply/')
def cls_apply(
        stone_mat_id: str,
        metal_mat_id: str,
        model: UploadFile = File(...)
):
    # Save usd
    model_bytes = model.file.read()
    model_path = './data/input/model.usd'

    with open(model_path, 'wb') as model_file:
        model_file.write(model_bytes)

    off_dir = './data/input/off'
    if not os.path.exists(off_dir):
        os.makedirs(off_dir)
    else:
        shutil.rmtree(off_dir)
        os.makedirs(off_dir)

    pcd_dir = './data/input/pcd'
    if not os.path.exists(pcd_dir):
        os.makedirs(pcd_dir)
    else:
        shutil.rmtree(pcd_dir)
        os.makedirs(pcd_dir)

    # Process model with Blender
    shell_script_path = './components/disassemble.sh'
    subprocess.run(['sh', shell_script_path])

    # Convert off data to point cloud with 8192 pts
    off2pcd()

    # Infer Pointnet2
    labels = infer()
    print(labels)

    # Apply materials
    materials_data = {}
    for k, v in labels.items():

        if v == 0:
            mat = stone_mat_id

        elif v == 1:
            mat = metal_mat_id

        materials_data[k.replace('model_', '')] = mat


    with open('components/apply_mat_multi.py', 'r') as apply_mat:
        apply_mat = apply_mat.read()
        apply_mat = apply_mat.replace('{{MAT_DATA}}', f'mat_data = {str(materials_data)}')

    with open('./apply_mat_exec_multi.py', 'w') as apply_mat_exec:
        apply_mat_exec.write(apply_mat)

    # Process model with Blender
    shell_script_path = './components/apply_mat_multi.sh'
    subprocess.run(['sh', shell_script_path])
