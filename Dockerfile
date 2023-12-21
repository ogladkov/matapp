FROM ubuntu:22.04

ENV PATH="/app/blender-4.0.2-linux-x64:${PATH}"

RUN apt-get update
RUN apt-get install python3 python3-pip gunicorn libgl1 libglib2.0-0 -y
RUN apt-get install tar curl libfontconfig1 libxrender1 libxi6 libgconf-2-4 libxkbcommon-x11-0 libsm6 libxext6 -y

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app files
COPY ./server.py /app/server.py
COPY ./components* /app/components
COPY ./data/METERIAL_METALICO.blend /app/data/METERIAL_METALICO.blend

WORKDIR /app

# Install Blender 4.0
RUN curl -o /app/blender.tar.xz -0 https://ftp.halifax.rwth-aachen.de/blender/release/Blender4.0/blender-4.0.2-linux-x64.tar.xz
RUN tar -xvf blender.tar.xz && rm blender.tar.xz

CMD [ "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]