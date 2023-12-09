#!/bin/bash

echo "Downloading Stanford NLP model..."
curl -OJL "https://huggingface.co/stanfordnlp/CoreNLP/resolve/main/stanford-corenlp-latest.zip"
unzip -o stanford-corenlp-latest.zip >/dev/null
mv stanford-corenlp-4.5.5 stanza_corenlp >/dev/null
unzip -o nltk_data.zip >/dev/null

# Build Docker image
docker build -t llama_fact_checker:latest .

echo "You will now be redirected to the container shell, the shell location is already inside the shared folder of the repo."

# Run the Docker image with shared folder
docker run -v "$(pwd)":/sharedFolder -it llama_fact_checker:latest /bin/bash
