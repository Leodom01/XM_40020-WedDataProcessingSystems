"""
Handles the input and output
"""
def load_data(input_path):
    data = {}
    with open(input_path) as openfileobject:
        for line in openfileobject:
            # skip empty lines
            if len(line) < 5:
                continue
            prts = line.rstrip().split()
            data[prts[0]] = {
                'Q': ' '.join(prts[1:])
            }
        openfileobject.close()
    return data

def output(data, out_path):
    with open(out_path, 'w') as fw:
        for qID in data.keys():
            fw.write(f"{qID}\tR\"{data[qID]['R']}\"\n")
            fw.write(f"{qID}\tA\"{data[qID]['A']}\"\n")
            fw.write(f"{qID}\tC\"{data[qID]['C']}\"\n")
            for ent in data[qID]['E']:
                fw.write(f"{qID}\tE\"{ent['name']}\"\t\"{ent['link']}\"\n")
