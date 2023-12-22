#!/bin/bash

git lfs clone https://huggingface.co/sentence-transformers/all-mpnet-base-v2 models/entity_linking_model
git lfs clone https://huggingface.co/deepset/roberta-base-squad2 models/entity_answer_extraction_model
git lfs clone https://huggingface.co/nfliu/roberta-large_boolq models/boolean_answer_extraction_model

curl -L -o ./models/stanford-corenlp-latest.zip "https://huggingface.co/stanfordnlp/CoreNLP/resolve/main/stanford-corenlp-latest.zip"
unzip -o ./models/stanford-corenlp-latest.zip -d ./models >/dev/null
echo "Stanford NLP model downloaded"

# Build Docker image
docker build -t llama_fact_checker:latest .

echo "You will now be redirected to the container shell, the shell location is already inside the shared folder of the repo."

# Run the Docker image with shared folder
docker run -v "$(pwd)":/sharedFolder -it llama_fact_checker:latest /bin/bash
