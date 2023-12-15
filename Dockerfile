FROM karmaresearch/wdps2

WORKDIR /sharedFolder
# Copy the current directory contents into the container at /app
COPY . /sharedFolder
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

RUN sudo apt -y update >/dev/null
RUN sudo apt install -y default-jre git-lfs>/dev/null

# Check if the directory is empty (the model could be taken from the shared folder)
RUN if [ -z "$(ls -A /sharedFolder/entity_linker_model)" ]; then \
      git clone https://huggingface.co/sentence-transformers/all-mpnet-base-v2 /sharedFolder/entity_linker_model; \
    fi

ENV NLTK_DATA=/sharedFolder/nltk_data
ENV CORENLP_HOME=/sharedFolder/stanza_corenlp

RUN python3 -m spacy download en