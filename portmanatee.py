import collections
import re

from nltk.corpus import wordnet as wn

def hypo(synset):
    return synset.hyponyms()

def hyper(synset):
    return synset.hypernyms()

def related(synset):
    return synset.also_sees() + synset.similar_tos()

def everything(synset):
    return related(synset) + hyper(synset) + hypo(synset)

def feelinglucky(syns):
    res = set(extract_words(syns))

    if len(res) > 100:
        return res
    res = res.union(extract_closures(syns, related, 4))

    if len(res) > 100:
        return res
    res = res.union(extract_closures(syns, hypo, 3))

    if len(res) > 5:
        return res
    res = res.union(extract_closures(syns, everything, 1))

    if len(res) > 5:
        return res
    res = res.union(extract_closures(syns, everything, 2))

    if len(res) > 5:
        return res
    res = res.union(extract_closures(syns, everything, 3))

    return res

def extract_closures(syns, fn, depth):
    s = set()
    for syn in syns:
        s = s.union(extract_words(syn.closure(fn, depth=depth)))
    return s

def extract_words(syns):
    words = set()
    for syn in syns:
        for word in syn.lemma_names():
            words.add(word)
    return set(filter_words(words))

def filter_words(wurds):
    return [wi for wi in wurds if not '_' in wi and not ' ' in wi]

def good_synonyms(wurd):
    return [syn for syn in synonyms(wurd) if not ' ' in syn]

def pronunciations(wurd):
    return phonemes().get(wurd.upper(), [])

PHONEMES_DICT = None
def phonemes():
    global PHONEMES_DICT
    if PHONEMES_DICT is None:
        PHONEMES_DICT = load_phonemes(open('cmudict-0.7b.txt'))
    return PHONEMES_DICT

def load_phonemes(file):
    phonemes = collections.defaultdict(list)
    for line in file:
        if line.startswith(';;;'):
            continue
        if not re.match(r'[A-Z]', line):
            continue
        res = load_phoneme(line)
        if len(res) != 2:
            print line
            print res
        phonemes[res[0]].append(res[1])
    res = load_phoneme('ADDEPAR  AE1 D AH1 P AA1 R')
    phonemes[res[0]].append(res[1])
    return phonemes

def load_phoneme(line):
    '''return ('wurd', ('ab', 'd', 'qr'))'''
    tokens = re.sub(r'[0-9]', '', line).split()
    wurd = tokens[0].split('(')[0]
    return (wurd, tuple(tok for tok in tokens[1:] if tok))

def match_score(p1, p2):
    n = min(len(p1), len(p2))
    for i in xrange(n, 0, -1):
        s = match(p1[-i:], p2[:i])
        if s > 0:
            return s
    return 0

def match(p1, p2):
    if p1 == p2:
        return len(p1) + (count_vowels(p1) * 2)
    score = 0
    for p1i, p2i in zip(p1, p2):
        si = match_single(p1i, p2i)
        if si == 0:
            return 0
        score += si
    return score

def count_vowels(ps):
    return sum(is_vowel(x) for x in ps)

def is_vowel(x):
    return 'A' in x or 'E' in x or 'I' in x or 'O' in x or 'U' in x

MATCH_PAIRS = set([
        ('AE', 'AH'),
        ('AA', 'IH'),
])
def match_single(x, y):
    if x == y:
        return 3 if is_vowel(x) else 1
    return 3 if (x, y) in MATCH_PAIRS or (y, x) in MATCH_PAIRS else 0

def length_score(w1, w2):
    return (len(w1) + len(w2)) / 10

def calculate_match_scores(wurds1, wurds2):
    scores = collections.defaultdict(lambda: 0)
    for w1 in wurds1:
        for w2 in wurds2:
            if w1 in w2 or w2 in w1:
                continue

            l = length_score(w1, w2)
            key = (w1, w2)
            p1 = pronunciations(w1)
            p2 = pronunciations(w2)

            for p1i in p1:
                for p2i in p2:
                    score = match_score(p1i, p2i)
                    if score > 0:
                        score += l
                    scores[key] = max(scores[key], score)
    return scores

def find_matches(wurds1, wurds2, thresh=1):
    scores1 = calculate_match_scores(wurds1, wurds2)
    scores2 = calculate_match_scores(wurds2, wurds1)

    results = [k + (v,) for k, v in scores1.iteritems() if v > thresh]
    results += [k + (v,) for k, v in scores2.iteritems() if v > thresh]
    results.sort(key=lambda t: t[2])
    return results

def go(syns1, syns2):
    if isinstance(syns1, str):
        syn1 = [syns1]
    else:
        syn1 = filter_words(feelinglucky(syns1))
    if isinstance(syns2, str):
        syn2 = [syns2]
    else:
        syn2 = filter_words(feelinglucky(syns2))

    print
    print sorted(syn1)
    print sorted(syn2)
    print

    return find_matches(syn1, syn2)

def choose_syns(wurd):
    syns = wn.synsets(wurd)
    if len(syns) == 0:
        return wurd
    if len(syns) == 1:
        return syns
    print 'choose the meanings of ' + wurd
    for i, syn in enumerate(syns):
        print i, syn.definition()
    choices = raw_input('choose plz\n').strip()
    if not choices:
        return syns

    choices = choices.split(',')
    choices = [int(x) for x in choices if x]

    result = []
    for choice in choices:
        result.append(syns[choice])
    return result

def synsets(wurd):
    return wn.synsets(wurd)

def synset(id):
    return wn.synset(id)

def init():
    phonemes()
    wn.synsets('dog')

def main(args):
    syns1 = choose_syns(args[1])
    syns2 = choose_syns(args[2])

    for line in go(syns1, syns2):
        print line

if __name__ == '__main__':
    import sys

    main(sys.argv)

