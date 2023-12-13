import subprocess

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse


# Start app
app = FastAPI()


@app.post('/main/')
def main(mat_id: str, data: UploadFile = File(...)):
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
