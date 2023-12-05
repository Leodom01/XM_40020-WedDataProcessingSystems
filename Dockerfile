FROM karmaresearch/wdps2

WORKDIR /sharedFolder
# Copy the current directory contents into the container at /app
COPY . /sharedFolder

# Install any needed packages specified in requirements.txt

RUN pip install -r requirements.txt