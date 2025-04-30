# # FROM python:3.11-slim

# # WORKDIR /app

# # # Copy requirements file
# # COPY requirements.txt .

# # # Install dependencies
# # RUN pip install --no-cache-dir -r requirements.txt

# # # Copy application code
# # COPY . .

# # # Expose Streamlit port
# # EXPOSE 8501

# # # Command to run the application
# # CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"] 
# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Expose the port Streamlit runs on (default 8501)
EXPOSE 8501

# Environment variables (optional, adjust based on .env)
ENV DB_USER=Pema
ENV DB_PASSWORD=delusional
ENV DB_HOST=localhost
ENV DB_PORT=5433
ENV DB_NAME=AgileDB

# Run the Streamlit app with explicit app.py
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# # Use an official Python runtime as a parent image
# FROM python:3.12-slim

# # Set working directory in the container
# WORKDIR /app

# # Copy the requirements file into the container
# COPY requirements.txt .

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the entire project directory into the container
# COPY . .

# # Expose the port Streamlit runs on (default 8501)
# EXPOSE 8501

# # Run the Streamlit app with explicit app.py
# CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]