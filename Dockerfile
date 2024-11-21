# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install FastAPI and Uvicorn
RUN pip install -r requierements.txt

# Make port 3500 available to the world outside this container
EXPOSE 3500

# Run app with Uvicorn on container startup
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3500"]
#CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "3500"]
