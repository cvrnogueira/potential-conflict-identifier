"""
    This algorithm receives as input a contract path and returns potential conflicting norms.
"""
from sentence_similarity import semantic_similarity
from norm_classifier import *
from extracting_parties import *
import hashlib

class Conflict_finder:

    def __init__(self):
        self.classifier = Classifier()      # Sentence classifier, which classifies a sentence either as norm or non-norm.
        self.party_norms = [[], []]           # Stores the norms applied to each party in the contract.
        self.modalVerbs = ['can', 'could', 'may', 'might', 'must', 'shall', 'should', 'will', 'ought']
        self.modal_dict = {
            'can'        :'permission',
            'may'        :'permission',
            'might'      :'permission',
            'could'      :'permission',
            'shall'      :'obligation',
            'must'       :'obligation',
            'will'       :'obligation',
            'ought'      :'obligation',        
            'should'     :'obligation',
            'shall not'  :'prohibition',
            'cannot'     :'prohibition',
            'could not'  :'prohibition',
            'might not'  :'prohibition',
            'may not'    :'prohibition', 
            'will not'   :'prohibition',
            'must not'   :'prohibition',
            'ought not'  :'prohibition',
            'should not' :'prohibition'            
        }

    def process(self, path):
        self.path = path
        self.read_contract()
        self.extract_contractual_norms()
        self.extract_entities()
        self.select_norms()
        return self.calculate_similarity()

    def read_contract(self, *path):
        # Reads a contract from a given path saving the sentences in a dictionary.
        if path:
            self.path = path[0]
        sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.contract_text = open(self.path, 'r').read()
        self.contract_sentences = sent_tokenizer.tokenize(self.contract_text)
        self.dict = {}
        for sentence in self.contract_sentences:
            key = hashlib.md5(sentence).digest()
            self.dict[key] = sentence

    def extract_contractual_norms(self, *text):
        # From the extracted contract text it obtains the norms.
        if text:
            self.read_contract(text[0])
        self.norms = self.classifier.extract_norms(self.contract_sentences)
    
    def extract_entities(self, *path):
        # Using a contract path, it extracts the entities and their nicknames, if it exists.        
        if path:
            self.path = path[0]
        self.entities, self.nicknames = extract_parties(self.path)
        
    def calculate_similarity(self):
        # Calculates the similartity between two sentences based on the Wordnet WUP measure.
        potential_conflicts = []
        index = 0
        text = ""
        for norm in self.party_norms:
            # Get a list of norms applied to the party.
            # Each element of the list is a tuple with (norm, modality_of_the_norm).
            text += "Presenting results for norms related to " + self.entities[index] + "\n"
            index += 1
            for i in range(len(norm)):
                # From the list of norms, execute two loops to compare them and extract their semantic similarity.
                ind = self.identify_modal(norm[i][0], True)     # Get index of the modal verb in the norm.
                norm1 = norm[i][0].split()                      # Get the norm (first position of the tuple) as a list of terms.
                norm1 = ' '.join(norm1[ind+1:])                 # From the modal verb point, turn the list elements into text.
                for j in range(len(norm)):
                    if j > i:
                        # Here we do the same process of above, just ensuring that we do not compare the same norms.
                        ind = self.identify_modal(norm[j][0], True)
                        label = self.compare_modalities(norm[i][1], norm[j][1])     # Defide the type of possible conflict according to the norms' modalities.
                        if label:
                            # If the pair of norms fits into one of the conflict types, 
                            norm2 = norm[j][0].split()
                            norm2 = ' '.join(norm2[ind+1:])
                            result = semantic_similarity.similarity(norm1, norm2)     # Get similarity.
                            if result >= 0.6:
                                # If similarity is lower or equal 0.6, we add it as a conflict.
                                text += "Similarity:" + str(result) + "\tLabel: " + str(label) + "\n"
                                text += norm[i][0] + "\n"
                                text += norm[j][0]
                                text += "\n-----------------\n"
        return text            

    def compare_modalities(self, mod1, mod2):
        # Compare the modalities and return their conflict type, if it exists.
        if (mod1 == "permission" and mod2 == "prohibition") or (mod2 == "permission" and mod1 == "prohibition"):
            return "Type 1"
        elif (mod1 == "permission" and mod2 == "obligation") or (mod2 == "permission" and mod1 == "obligation"):
            return "Type 2"
        elif (mod1 == "obligation" and mod2 == "prohibition") or (mod2 == "obligation" and mod1 == "prohibition"):
            return "Type 3"
        else:
            return 0
        
    def select_norms(self):
        # From norms, it extracts the ones that have at least one modal verb and then identifies the entity.
        for norm in self.norms:
            index = self.identify_modal(norm, True)
            norm = norm.split()
            if not index:
                continue
            for element in norm[:index][::-1]:  # Go through the words before the modal verb, which we believe is described te party name.
                if self.find_nickname(element, norm):
                    break
                if self.find_entity(element, norm):
                    break

    def find_nickname(self, element, norm):
        for word in self.nicknames:
            for w in word.split():
                if w.lower() == element.lower():
                    self.create_norm_list(self.nicknames.index(word), ' '.join(norm))
                    return True
        return False
    
    def find_entity(self, element, norm):
        for word in self.entities:
            for w in word.split():
                if w.lower() == element.lower():
                    self.create_norm_list(self.entities.index(word), ' '.join(norm))
                    return True
        return False

    def identify_modal(self, *info):
        # Identifies the index in which the modal is placed in the norm when receiving more than one parameter
        # Returns the norm modality
        index = None
        norm = info[0]
        norm = norm.split()
        for verb in self.modalVerbs:
            if verb in norm:
                modal_verb = verb
                index = norm.index(verb)
                break
        if info[1]:
            if index:
                return index
            else:
                False

        else:
            if norm[index + 1] == 'not':
                modal_verb = modal_verb + ' not'

            modality = self.modal_dict[modal_verb]
            
            return (info[0], modality)

    def create_norm_list(self, entity_num, norm):
        # Fulfill the ent_norm list according to the selected entity
        self.party_norms[entity_num].append(self.identify_modal(norm, False))

if __name__ == "__main__":
    finder = Conflict_finder()
    print finder.process("data/ContractTest/Chang-03_07_2015-15:49:42/aortech.mfg.1998.12.23.shtml")