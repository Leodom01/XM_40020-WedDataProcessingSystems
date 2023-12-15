FROM karmaresearch/wdps2

WORKDIR /sharedFolder
# Copy the current directory contents into the container at /app
COPY . /sharedFolder
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN pip install spacy

RUN sudo apt -y update >/dev/null
RUN sudo apt install -y default-jre>/dev/null
RUN sudo apt install -y git-lfs>/dev/null
RUN git lfs install

ENV NLTK_DATA=/sharedFolder/nltk_data
ENV CORENLP_HOME=/sharedFolder/stanza_corenlp

RUN python3 -m spacy download en