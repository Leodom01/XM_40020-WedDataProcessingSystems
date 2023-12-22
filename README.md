
# XM_40020-WedDataProcessingSystems

## Description
The project implements a pipeline to fact check the answer of a LLM (LLaMa) by using Wikidata as a knowledge base.

Given an input file in the format: <ID question><TAB><question><newline> 
We will return a file with formatting: <ID question><TAB>[R,A,C,E]<value>
Where:
"R" has the value the raw text produced by the language model.

"A" has the extracted answer distilled from the LLM answer.

"C" is the tag correct/incorrect, the outcome of the fact checking.

"E" are the entities extracted and linked to Wikipedia, both from question and answer.

Further technical details can be found in report.pdf
Be aware: all the project data and files can be found in the /sharedFolder of the docker container, we write nowhere else.

## Run container

In order to run the image of the project you will need to pull the docker image and run the interactiveDemo.py script:
```bash
  # From your machine
  docker pull leodom01/webdataprocessingsystems_factchecker
  docker run -it leodom01/webdataprocessingsystems_factchecker /bin/bash
  # Within the container
  cd /sharedFolder
  python3 interactiveDemo.py 
```
The scripts use by default input and output file: task_data/example_input.txt and task_data/example_output.txt .
In case you want to use different input and output files you can run:
```bash
  # Within the container
  python3 interactiveDemo.py /sharedFolder/task_data/my_input.txt /sharedFolder/task_data/my_output.txt
```
To copy files from your local machine you can use:
```bash
  # From your machine
  docker cp ./inputfile.txt CONTAINER:/sharedFolder/task_data/my_input.txt
```

## Build image (just in the case the docker image is not working straight away)
In order to build the image you'll need to have the following tools installed on your machine. We use them to fetch the models:
```bash
  curl
  unzip
  git lfs
```
With the buildAndStartContainer.sh file you can automatically download the needed models, build the image and be spawned inside the running container (may take a while due to the models size):
```bash
  sh ./buildAndStartContainer.sh
```

## Python project file running
In case the input file and output file aren't defined the script will read from /sharedFolder/task_data/example_input.txt and write to /sharedFolder/task_data/example_output.txt
```python
python3 interactiveDemo.py <input file> <output file>
```
During the run the script will print logs to console, the "official" output will always be found in the output file tho.