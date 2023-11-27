#AI GENERATED DO NOT SUBMIT

# Import the spaCy library
import spacy

# Load the English language model
nlp = spacy.load('en_core_web_sm')

# Define the text
text = "Apple Inc. is planning to open a new store in San Francisco on January 1, 2024."

# Process the text
doc = nlp(text)

# Print the entities
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)