import re
import spacy


class FileParser:

    def __init__(self):
        self.nlp = spacy.load("en")
        #self.nlp = spacy.load('en_core_web_sm')

    def parse_key_file(self, fp):
        """
        Parses a "gold answer" key file.
        Takes a key file path and returns a dictionary, with
        the coref ID as the key and the value as a list of
        tuples, of the form (full_coref, head_of_coref)
        """
        coref_pattern = "<COREF ID=\"(X[0-9]+)\">(.*?)</COREF>"
        key_pattern = "^{(.*?)} {(.*?)} {(.*?)}"

        gold_answers = {}
        c_id = None
        with open(fp) as f:
            for line in f:

                # Blank Line
                if line == "\n":
                    continue

                coref = re.findall(coref_pattern, line)

                # New Coref to process
                if len(coref) > 0:
                    c_id, c_word = coref[0]
                    try:
                        c_word = next(self.nlp(c_word).noun_chunks).root.text
                    except StopIteration:
                        pass

                    gold_answers[c_id] = {"orig": c_word, "corefs": []}

                # Instance of Coref
                else:

                    key_values = re.match(key_pattern, line)
                    s_id = key_values.group(1)
                    word = key_values.group(3)

                    gold_answers[c_id]['corefs'].append((s_id, word))

        return gold_answers

    def parse_input_file(self, fp):

        output = {
            "sentences": {},
            "corefs": {},
            "noun_phrases": {}
        }

        sent_tag_pattern = "<S ID=\"([0-9]+)\">(.*)</S>"
        coref_pattern = "<COREF ID=\"(X[0-9]+)\">(.*?)</COREF>"
        any_tag_pattern = "<[^<]+?>"

        with open(fp) as f:
            for line in f:
                sent_re = re.match(sent_tag_pattern, line)
                sent_id = sent_re.group(1)
                sent = sent_re.group(2)

                coref_re = re.findall(coref_pattern, sent)
                for c_id, c_word in coref_re:
                    output['corefs'][c_id] = (c_word,sent_id)

                sent = re.sub(any_tag_pattern, '', sent)
                output['sentences'][sent_id] = sent
                output['noun_phrases'][sent_id] = self._extract_noun_phrases(sent)

        return output

    def _extract_noun_phrases(self, sent):
        noun_phrases = []
        n_chunks = self.nlp(sent).noun_chunks
        for np in n_chunks:
            root = np.root.text
            noun_phrases.append({"np": np, "root": root})

        return noun_phrases