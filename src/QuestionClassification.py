import spacy
"""
This module classifies the input questions
"""
def classify_question(question):
    """
    Classifies a given question based on keywords present in the question.

    Parameters:
    question (str): The input question to be classified.

    Returns:
    str: A string representing the category of the question.
         Possible values:
         - 'Boolean' if the question starts with a boolean keyword.
         - 'Entity' if the question contains WH words.
         - 'Completion' if the question doesn't match the above criteria.
    """
    nlp = spacy.load("en_core_web_sm")
    # Using spacy tokenizer
    doc = nlp(question)

    entity_keywords = ['who', 'what', 'where', 'when', 'why', 'which', 'whom', 'whose']
    boolean_keywords = ['is', 'are', 'do', 'does', 'can', 'will', 'could', 'should',
                        'would', 'has', 'have', 'yes', 'no', 'was', 'were', 'did', 'may']
    if doc[0].text.lower() in boolean_keywords:
        return 'Boolean'
    # Iterate through tokens in the sentence
    for token in doc:
        if token.text.lower() in entity_keywords:
            return 'Entity'
    return 'Completion'
