import random
from collections import Counter


connections = {
    'a': 'defhjklmnpqrstvwxzy',
    'b': 'aceilorsuy',
    'c': 'aeiloruvy',
    'd': 'aeilorsuy',
    'e': 'abcdfghlmnoprstvxz',
    'f': 'aeilortuyj',
    'g': 'aeilnorsuvy',
    'h': 'aeioruvy',
    'i': 'acdefgklmnoprstvwz',
    'j': 'aeouy',
    'k': 'aeilorstvwy',
    'l': 'aeiouy',
    'm': 'aeiorsuy',
    'n': 'aeiouy',
    'o': 'bcdfgjklmnprstvwxzy',
    'p': 'aehiorstuy',
    'q': 'aeiou',
    'r': 'aeiovuy',
    's': 'acefhilnoprtuvy',
    't': 'acefhiorsuvyz',
    'u': 'bdklprstvjwxz',
    'v': 'aceijlnoruy',
    'w': 'aeijnoruy',
    'x': 'aeiouy',
    'y': 'aoes',
    'z': 'aeouy',
}


vowels = 'aeiouy'

# min and max length of a nick
nick_len = [6,8]

# how many times the same character may occur
max_occur = 2

# targeted consonants/vowels ratio
target_ratio = 1.6

# following characters will not occur in nick
excluded = 'qvxy'

# at least one of following characters will occur in nick
included = ''

# nick will not start with following characters
not_start = vowels+'x'

# nick will not end with following characters
not_end = ''


def get_ratio(sequence):
    amount_vowels = len([char for char in sequence if char in vowels]) or 1
    return (len(sequence)-amount_vowels)/amount_vowels


def get_next_random(s):
    _choice = connections.get(s)
    assert(_choice)
    rand = random.choice(_choice)
    for ex in excluded or ['']:
        if ex == rand:
            return get_next_random(s)
    return rand


def gen_nick():

    chain = random.choice(list(connections.keys()))

    for ex in (excluded or '') + (not_start or ''):
        if ex == chain:
            return gen_nick()

    for _ in range(random.randint(*nick_len)-1):
        last = chain[-1]
        rand = get_next_random(last)
        if len(chain) > 1:
            while True:
                if chain[-2] != rand:
                    break
                else:
                    rand = get_next_random(last)
        chain += rand

    if not any(inc in chain for inc in included or ['']) or get_ratio(chain) > target_ratio or max(Counter(chain).values()) > max_occur or any(c == chain[-1] for c in not_end or ['']):
        return gen_nick()

    return chain.capitalize()
