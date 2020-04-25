import nltk
from nltk.parse.corenlp import CoreNLPServer
from  nltk.parse.corenlp import CoreNLPParser
import spacy
import os
import requests
from nltk.tree import Tree
from nltk.draw.tree import TreeView

STANFORD = os.path.join("models", "stanford-corenlp-full-2018-10-05")
server = CoreNLPServer(
   os.path.join(STANFORD, "stanford-corenlp-3.9.2.jar"),
   os.path.join(STANFORD, "stanford-corenlp-3.9.2-models.jar"),    
)
'''
filenames = ["a1.txt","a2.txt","a3.txt","a4.txt","a5.txt","a6.txt","a7.txt","a8.txt","a9.txt","a10.txt"]
datum = ""

for filename in filenames:
    with open(filename,"r") as f:
        datum += f.read()
'''
import wikipedia
datum = (wikipedia.page(title="School").content)
#doc = nlp(datum)

(requests.post('http://[::]:9000/?properties={"annotators":"tokenize,ssplit,pos","outputFormat":"json"}', data = {'data': datum}).text)
#server.start()

question = []
nlp = spacy.load('en_core_web_sm')

parser = CoreNLPParser()
parse = next(parser.raw_parse("I put the book in the box on the table."))

class SST():
    def __init__(self, label, children):
        self.label = label
        self.children = children


# Sentence Structure Leaf
class SSL():
    def __init__(self, label):
        self.label = label

simple_predicate = SST('ROOT', [SST('S', [SSL('NP'), SSL('VP'), SSL('.')])])

def list_to_string(word_list):
    return ' '.join(word_list)

def satisfies_structure(parsed_tree, structure):
    if isinstance(structure, SSL):
        return parsed_tree.label() == structure.label
    else:
        if parsed_tree.label() != structure.label or len(parsed_tree) != len(structure.children): return False
        for i in range(len(parsed_tree)):
            if satisfies_structure(parsed_tree[i], structure.children[i]) == False:
                return False
        return True

def tree_to_string(parsed_tree):
    #     if isinstance(parsed_tree, str):
    #         return parsed_tree
    #     words = []
    #     for subtree in parsed_tree:
    #         words.append(tree_to_string(subtree))
    return list_to_string(parsed_tree.leaves())

def traverse(t):
    try:
        t.label()
    except AttributeError:
        print(t, end=" ")
    else:
        # Now we know that t.node is defined
        print('(', t.label(), end=" ")
        for child in t:
            traverse(child)
        print(')', end=" ")

def WH_question_from_tree(parsed_tree):
    sentence = parsed_tree[0]
    assert (sentence.label() == 'S')
    np = sentence[0]
    vp = sentence[1]
    '''
    print((np.leaves()))
    print((vp.leaves()))
    print(np.label())
    print(vp.label())'''

    vpWord = " ".join(vp.leaves())
    npWord = " ".join(np.leaves())
    doc = nlp(npWord)
    #print(f'ents : {npSpacy.ents}')
    for ent in doc.ents:
        print(f'ent text : {ent.text}\n')
        print(f'ent label : {ent.label}\n')
        text = ent.text
        label = ent.label
        if label =="GPE":
            question.append(f"Where {npWord} {vpWord} ?")
        elif label == 383 or label == 380: #"PERSON":
            question.append(f"What {vpWord}?")
        elif label == 381: # "People":
            question.append(f"Who {vpWord} ?")

    innerNPtype = np[0].label()
    #innerNPtype2 = np[0][0].label()
    #question.append(f"What {npWord} {vpWord} ?")
    #question.append(f"Did {npWord} {vpWord} ?")
    if innerNPtype == "CD":
        question.append(f"How many {npWord} ?")
    if innerNPtype == "NNS":
        #question.append(f"Who are {npWord} ?")
        question.append(f"What are {npWord} ?")
        question.append(f"What {npWord} {vpWord} ?")
        question.append(f"Why do {npWord} {vpWord} ?")
    assert (np.label() == 'NP')
    assert (vp.label() == 'VP')
    '''
    if vp[0].label() == 'VBZ':
        return list_to_string([vp[0][0].capitalize(), tree_to_string(np), tree_to_string(vp[1])]) + '?'
        '''
    return None #vp[0]
'''
url = "http://localhost:9000/tregex"
apposition_pattern = "NP !< CC !< CONJP < (NP=np1 $.. (/,/ $.. (NP=app $.. /,/)))"
verb_modifier_pattern = "NP=noun > NP $.. VP=modifier"
r = requests.post(url, data=text, params={"pattern":apposition_pattern})
print(f'apposition {r}')
'''
sentences = nltk.sent_tokenize(datum)
questions_made = 0
nquestions = 10
parse_list = []
for sentence in sentences:
    if len(sentence) < 180:
        parse = next(parser.raw_parse(sentence))
        if satisfies_structure(parse, simple_predicate):
            WH_question_from_tree(parse)
            parse_list.append(parse)
            questions_made+=1
    if questions_made == nquestions:
        break
'''
f = open("more_example.txt", "a")
for q in set(question):
    f.write(q+"\n")
f.close()'''
print(set(question))
