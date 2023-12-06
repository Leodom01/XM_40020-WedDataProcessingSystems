
# XM_40020-WedDataProcessingSystems

Given input: <ID quest!on><TAB>text of the question/comple!on<newline> 

will return a file with formatting: <ID ques!on><TAB>[R,A,C,E]<answer>

where:

"R" indicates the raw text produced by the language model, 

"A" is the extracted answer

"C" is the tag correct/incorrect

"E" are the entities extracted.


## Stack

NLTK (preprocessing) https://www.nltk.org

Spacy (NER) https://spacy.io

OpenRE
## Installation

enter the directory where you downloaded the dockerfile and run

```bash
  docker build -t image_name . 
```

dockerfile will download dependencies from requirements.txt

run the image just created

```bash
docker run image_name
```
## Usage/Examples

```python
python3 interactiveDemo.py
```


## Schema



