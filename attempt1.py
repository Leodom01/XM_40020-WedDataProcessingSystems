#used ai in some sections do not submit as it is

import nltk
from nltk.corpus import stopwords
import spacy

nlp = spacy.load("en_core_web_sm")

nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))


def ner_on_question(question,wiki):

    array_question_labels=[]
    array_question_content=[]
    array_text_labels=[]
    array_text_content=[]

    nlp = spacy.load("en_core_web_sm")

    doc_question = nlp(question)

    print(f"Original section QUESTION: {question}")
    #print("Entities:")

    for entity in doc_question.ents:
        ##print(entity.text, entity.label_)
        #print("\n")
        array_question_labels.append(entity.label_)
        array_question_content.append(lemmatized(entity.text))
   

    sections_wiki = wiki.split(".")

    for section in sections_wiki:
        array_text_labels=[]
        array_text_content=[]
        
        doc = nlp(section)

        ##print(f"Original section checking now: {section} -------------------")
        ##print("Entities:")

        for entity in doc.ents:
            ##print(entity.text, entity.label_)
            #print("\n")
            array_text_labels.append(entity.label_)
            array_text_content.append(lemmatized(entity.text))
            

        if check_arrays(array_text_labels,array_question_labels):
            if check_arrays(array_text_content,array_question_content):
                print("---------------------------------------------")
                print("---------------------------------------------")
                print("its a match")
                print("ON Text")
                print("array_text_content: "+str(array_text_content))
                print("array_question_content: "+str(array_question_content))
                print("ON Labels")
                print("array_text_labels: "+str(array_text_labels))
                print("array_question_labels: "+str(array_question_labels))
                print("---------------------------------------------")
                print("---------------------------------------------")
                
            ##else:
                ##print("NO match content")
                #print("array_text_content"+str(array_text_content))
                #print("array_question_content"+str(array_question_content))
                
                
        ##else:
            ##print("NO match labels")



def check_arrays(text, question):
    return set(question).issubset(set(text))


def lemmatized(text):
    doc = nlp(text)
    lemmatized_text = ' '.join([token.lemma_ for token in doc])
    return lemmatized_text
