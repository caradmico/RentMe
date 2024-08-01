# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . /app/

# Copy the environment file
COPY .env /app/.env

# Set environment variables
ENV DB_NAME=your_database_name \
    DB_USER=your_database_user \
    DB_PASSWORD=your_database_password \
    DB_HOST=your_database_host \
    DB_PORT=your_database_port

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "houseme_project.wsgi:application"]
