FROM karmaresearch/wdps2

WORKDIR /sharedFolder
# Copy the current directory contents into the container at /app
COPY . /sharedFolder
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

RUN sudo apt -y update >/dev/null
RUN sudo apt install -y default-jre >/dev/null

ENV NLTK_DATA=/sharedFolder/nltk_data
ENV CORENLP_HOME=/sharedFolder/stanza_corenlp

RUN python3 -m spacy download en