# A simple basic question classification based on rules.
# If higher accuracy is our goal, we can maybe look into ML models and other sophisticated methods for this task.
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

    return 'Entity'

if __name__ == "__main__":
    import LoadTestData
    questions = LoadTestData.loadBoolQ('../task_data/boolq_train.jsonl')
    # questions = [data[x]['Q'] for x in data.keys()]
    for q in questions:
        classification = classify_question(q)
        str = f'Question: "{q}" - Classification: {classification}'
        if classification == 'Entity' : str = str + '<================'
        print(str)
