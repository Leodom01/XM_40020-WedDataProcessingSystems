# TODO: implement a more sophisticated approach for question classification
# Boolean questions require yes/no answers, starting with is, are, do, does, etc.
# Entity questions usually contain wh words. What, where, whose, etc.
# Completion questions, like entity questions, require an entity in answer.
def classify_question(question):
    boolean_keywords = ['is', 'are', 'do', 'does', 'can', 'will', 'could', 'should',
                        'would', 'has', 'have', 'yes', 'no', 'was', 'were', 'did', 'may']
    entity_keywords = ['who', 'what', 'where', 'when', 'why', 'which', 'whom', 'whose']

    words = question.lower().split()

    for word in words:
        if word in boolean_keywords:
            return 'Boolean'
        elif word in entity_keywords:
            return 'Entity'

    return 'Completion'

if __name__ == "__main__":
    pass
