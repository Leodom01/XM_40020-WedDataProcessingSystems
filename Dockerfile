FROM karmaresearch/wdps2

WORKDIR /sharedFolder
# Copy the current directory contents into the container at /app
COPY . /sharedFolder

RUN sudo apt update
RUN sudo apt install -y default-jre
# Install any needed packages specified in requirements.txt

RUN pip install -r requirements.txt

RUN python3 -m spacy download en
