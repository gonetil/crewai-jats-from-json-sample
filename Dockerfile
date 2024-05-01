# Use the Python 3.11 slim base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt ./

# Install Python dependencies from requirements file
RUN pip install -r requirements.txt
RUN python3 -m pip install --user pipx
RUN python3 -m pipx ensurepath


# Keep the container running
CMD ["tail", "-f", "/dev/null"]


#docker build -t crewai .
