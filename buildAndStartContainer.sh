#!/bin/bash

echo "Downloading Stanford NLP model..."
curl -OJL "https://huggingface.co/stanfordnlp/CoreNLP/resolve/main/stanford-corenlp-latest.zip"
unzip -o stanford-corenlp-latest.zip >/dev/null
rm stanford-corenlp-latest.zip
mv stanford-corenlp-4.5.5 stanza_corenlp >/dev/null
unzip -o nltk_data.zip >/dev/null
git lfs clone https://huggingface.co/sentence-transformers/all-mpnet-base-v2 models/entity_linking_model
git lfs clone https://huggingface.co/deepset/roberta-base-squad2 models/entity_answer_extraction_model
git lfs clone https://huggingface.co/nfliu/roberta-large_boolq models/boolean_answer_extraction_model

# Build Docker image
docker build -t llama_fact_checker:latest .

echo "You will now be redirected to the container shell, the shell location is already inside the shared folder of the repo."

# Run the Docker image with shared folder
docker run -v "$(pwd)":/sharedFolder -it llama_fact_checker:latest /bin/bash
