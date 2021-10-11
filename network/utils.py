from nltk.corpus import wordnet as wn
import nltk
nltk.download('wordnet')


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


pos_tag_map = {
    'CC': None,  # coordin. conjunction (and, but, or)
    'CD': wn.NOUN,  # cardinal number (one, two)
    'DT': None,  # determiner (a, the)
    'EX': wn.ADV,  # existential ‘there’ (there)
    'FW': None,  # foreign word (mea culpa)
    'IN': wn.ADV,  # preposition/sub-conj (of, in, by)
    'JJ': wn.ADJ,
    'JJR': wn.ADJ,  # adj., comparative (bigger)
    'JJS': wn.ADJ,  # adj., superlative (wildest)
    'LS': None,  # list item marker (1, 2, One)
    'MD': None,  # modal (can, should)
    'NN': wn.NOUN,  # noun, sing. or mass (llama)
    'NNS': wn.NOUN,  # noun, plural (llamas)
    'NNP': wn.NOUN,  # proper noun, sing. (IBM)
    'NNPS': wn.NOUN,  # proper noun, plural (Carolinas)
    'PDT': wn.ADJ,  # predeterminer (all, both)
    'POS': None,  # possessive ending (’s )
    'PRP': None,  # personal pronoun (I, you, he)
    'PRP$': None,  # possessive pronoun (your, one’s)
    'RB': wn.ADV,  # adverb (quickly, never)
    'RBR': wn.ADV,  # adverb, comparative (faster)
    'RBS': wn.ADV,  # adverb, superlative (fastest)
    'RP': wn.ADJ,  # particle (up, off)
    'SYM': None,  # symbol (+,%, &)
    'TO': None,  # “to” (to)
    'UH': None,  # interjection (ah, oops)
    'VB': wn.VERB,  # verb base form (eat)
    'VBD': wn.VERB,  # verb past tense (ate)
    'VBG': wn.VERB,  # verb gerund (eating)
    'VBN': wn.VERB,  # verb past participle (eaten)
    'VBP': wn.VERB,  # verb non-3sg pres (eat)
    'VBZ': wn.VERB,  # verb 3sg pres (eats)
    'WDT': None,  # wh-determiner (which, that)
    'WP': None,  # wh-pronoun (what, who)
    'WP$': None,  # possessive (wh- whose)
    'WRB': None,  # wh-adverb (how, where)
    ',': None,
    '?': None,
    '!': None,
    '.': None,
    '...': None,
    '"': None,
    '[': None,
    '{': None,
    ']': None,
    '}': None,
    '(': None,
    ')': None,
    "''": None,
    "'": None,
    "^": None,
    "|": None,

}
