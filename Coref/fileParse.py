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
        """
        Takes input file path and returns a dictionary, containing
        a dictionary of raw sentences (Sentence id as keys),
        a dictionary of sentence noun phrases (Sentence id as keys),
        a dictionary initial coreferences.
        Expected input file format: each sentence surrounded by
            <S ID="<id_num>"> ... </S>
        and each initial coreference surrounded by tags
            <COREF ID="X<coref_id_num>"> ... </COREF>
        For example, the following would be a valid input file, with initial
        corefs of
            "Susan Mills",
            "a home"
            "her dog".
        <S ID="0"><COREF ID="X0">Susan Mills</COREF>bought<COREF ID="X1">a home</COREF>in Utah.</S>
        <S ID="1">A nice feature is that the 2-story house has a big yard for<COREF ID="X2">her dog</COREF>.</S>
        <S ID="2">The German Shepherd weighs 100 lbs and is very active.</S>
        <S ID="3">Both Sue and the dog love the new house!</S>
        Output: 
            <sentences>    = Dictionary with key as the sentence id,
                             and value as the sentence (without any coreference tags)
            <corefs>       = Dictionary with key as coref id, and value as the
                             initial coreference string
            <noun_phrases> = Dictionary with key as the sentence id,
                             and value as a list of dictionaries, with the
                             keys 'np' (the full noun phrase) and 'root'
                             (root of the noun phrase)
        """

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