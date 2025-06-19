FROM python:3.11-slim

# Install system dependencies for camera and SPI, plus git, curl, etc
RUN apt-get update && apt-get install -y \
    libatlas-base-dev \
    libopenjp2-7 \
    libtiff5 \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libjpeg-dev \
    libv4l-dev \
    v4l-utils \
    libcamera-apps \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements & install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
