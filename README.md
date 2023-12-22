
# XM_40020-WedDataProcessingSystems

Given input: <ID quest!on><TAB>text of the question/comple!on<newline> 

will return a file with formatting: <ID ques!on><TAB>[R,A,C,E]<answer>

where:

"R" indicates the raw text produced by the language model, 

"A" is the extracted answer

"C" is the tag correct/incorrect

"E" are the entities extracted.

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
The scripts uses by default input and output file: task_data/example_input.txt and task_data/example_output.txt
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
In order to build the image you'll need to have the following tools in your machine, we need to fetch the models:
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



