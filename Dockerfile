FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Install dependencies for the system
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy 
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 8000

# Command to start the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
