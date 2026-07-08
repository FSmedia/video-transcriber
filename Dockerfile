# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies (ffmpeg is required for yt-dlp and whisper)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose ports for web apps
# Streamlit uses 8501
EXPOSE 8501
# Gradio typically uses 7860
EXPOSE 7860

# Default command: Run the Gradio app by default, but it can be overridden
CMD ["python", "app_gradio.py"]
