# Base Python image
FROM python:3.10.16-slim

# Set work directory
WORKDIR /app

# Copy requirements first and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project (including manage.py, your Django app, and docker/ scripts)
COPY . /app/

# Expose the Django port
EXPOSE 8000

# Make sure our scripts are executable
RUN chmod +x docker/create_products.sh
RUN chmod +x docker/start_server_setup_dummy_data.sh

# When the container starts, run our custom script
CMD ["sh", "docker/start_server_setup_dummy_data.sh"]
