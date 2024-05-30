# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    libxi-dev \
    libxrender-dev \
    libxi6 \
    libxrender1 \
    libfontconfig1 \
    libssl-dev \
    libxrandr2 \
    libxfixes3 \
    libxcursor1 \
    libxinerama1 \
    libglu1-mesa-dev \
    libgl1-mesa-dev \
    libglfw3 \
    libglfw3-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Clone Blender's source code
RUN git clone https://github.com/blender/blender.git
WORKDIR /usr/src/app/blender

# Run Blender's build scripts to build bpy
RUN make bpy

# Install the bpy module to the Python environment
RUN make install

# Set the Python path to include the bpy module
ENV PYTHONPATH="/usr/src/app/blender/build_linux_bpy/lib:${PYTHONPATH}"

# Copy the rest of your application's code
COPY . .

# Run your Python application
CMD ["python", "your_script.py"]
