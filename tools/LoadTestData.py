# simple utility functions to load the test data
import json


def load_data(input_path):
    data = {}
    with open(input_path) as openfileobject:
        for line in openfileobject:
            prts = line.rstrip().split('\t')
            data[prts[0]] = {
                'Q': prts[1]
            }
        openfileobject.close()
    return data
def output(data, out_path):
    with open(out_path, 'w') as fw:
        for qID in data.keys():
            fw.write(f"{qID}\tR\"{data[qID]['R']}\n")
            fw.write(f"{qID}\tA\"{data[qID]['A']}\n")
            fw.write(f"{qID}\tC\"{data[qID]['C']}\n")
            for ent in data[qID]['E']:
                fw.write(f"{qID}\tE\"{ent['name']}\t{ent['link']}\n")



def fixtestformat(): # IGNORE this function
    data = {}
    with open('../task_data/example_in.txt') as openfileobject:
        for line in openfileobject:
            data[line[0:12]] = {
                'Q':line[12:].strip(),
                'R':'',
                'A':'',
                'C':'',
                'E':[]
            }
    with open('../task_data/example_out.txt') as openfileobject:
        for line in openfileobject:
            tmp2 = line[12:].strip()
            if tmp2[0] == 'R':
                data[line[0:12]]['R'] = line[12:].strip()
            if tmp2[0] == 'A':
                data[line[0:12]]['A'] = line[12:].strip()
            if tmp2[0] == 'C':
                data[line[0:12]]['C'] = line[12:].strip()
            if tmp2[0] == 'E':
                entlist = data[line[0:12]]['E']
                entlist.append(line[12:].strip())
                data[line[0:12]]['E'] = entlist

    #
    with open('../task_data/example_in.txt', 'w') as fw:
        for q in data.items():
            fw.write(f"{q[0]}\t{q[1]['Q']}\n")

    with open('../task_data/example_out.txt', 'w') as fw:
        for q in data.items():
            fw.write(f"{q[0]}\t{q[1]['R']}\n")
            fw.write(f"{q[0]}\t{q[1]['A']}\n")
            fw.write(f"{q[0]}\t{q[1]['C']}\n")
            for e in q[1]['E']:
                fw.write(f"{q[0]}\t{e}\n")


    print(data)

# def load_data(path_in, path_out):
#     data = {}
#     with open(path_in) as openfileobject:
#         for line in openfileobject:
#             prts = line.rstrip().split('\t')
#             data[prts[0]] = {
#                 'Q':prts[1]
#             }
#         openfileobject.close()
#     with open(path_out) as openfileobject:
#         for line in openfileobject:
#             prts = line.rstrip().split('\t')
#             if prts[1][0] == 'R':
#                 data[prts[0]]['R'] = prts[1][2:-1]
#             if prts[1][0] == 'A':
#                 data[prts[0]]['A'] = prts[1][2:-1]
#             if prts[1][0] == 'C':
#                 data[prts[0]]['C'] = prts[1][2:-1]
#             if prts[1][0] == 'E':
#                 entlist = data[prts[0]]['E']
#                 entlist.append(prts[1][2:-1])
#                 data[prts[0]]['E'] = entlist
#     return data

def loadFreebaseQA(path):
    f = open(path)
    data = json.load(f)
    questions = [x['RawQuestion'] for x in data['Questions']]
    return questions

def loadBoolQ(path):
    with open(path) as f:
        data = [json.loads(line) for line in f]
    questions = [x['question'] for x in data]
    return questions

if __name__ == "__main__":
    pass





