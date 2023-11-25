#!/bin/bash

# Build Docker image
docker build -t llama_fact_checker:latest .

echo "You will now be redirected to the container shell, the shell location is already inside the shared folder of the repo."

# Run the Docker image with shared folder
docker run -v "$(pwd)":/sharedFolder -it llama_fact_checker:latest /bin/bash
