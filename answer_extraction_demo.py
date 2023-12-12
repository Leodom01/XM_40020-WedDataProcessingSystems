# just a demo to showcase answer extraction. delete before submitting
import tools.LoadTestData as ltd
import tools.QuestionClassification as qc
import tools.AnswerExtraction as ae

data = ltd.load_data('task_data/example_in.txt', 'task_data/example_out.txt')
q = [data[x]['Q'] for x in data.keys()]
a = [data[x]['R'] for x in data.keys()]


for i in range(len(q)):
    print(f"q:{q[i]}, a:{a[i]}")
    if qc.classify_question(q[i]) == 'Boolean':
        print(ae.boolean_answer_extraction(q[i], a[i]))
    else:
        print(ae.entity_answer_extraction(q[i], a[i]))
    print("==========================")
