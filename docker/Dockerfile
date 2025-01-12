# Base Python image
FROM python:3.10.16-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file to the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Expose the port Django will run on
EXPOSE 8000

# Default command to run the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]