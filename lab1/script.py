'''
Usage: 
    ./script.py [-t TEXT] [-k TOP_K] [-n TOP_N]

Options:
    -t TEXT input text 
    -k number of printed ngrams
    -n number of characters for ngrams
'''

import sys
from statistics import median, mean
from more_itertools import take
from docopt import docopt

def count_words(text):
    word_counter = dict()
    for unstriped_word in text.split():
        word = unstriped_word.strip(',.').lower()
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1

    return word_counter

def count_words_in_sentence(text):
    words_in_sentence = list()

    for i in filter(None, text.split('.')):
        words_in_sentence.append(len(i.split()))
    
    return words_in_sentence

def avg_words_in_sentences(words_in_sentence):
    return int(mean(words_in_sentence))

def median_words_in_sentences(words_in_sentence):
    return int(median(words_in_sentence))

def top_k_of_top_n(text, k, n):
    ngrams = dict()

    for unstriped_word in text.split():
        word = unstriped_word.strip(',.').lower()
        for i in range(len(word)-n+1):
            gram = word[0+i:n+i]
            if gram in ngrams:
                ngrams[gram] += 1
            else:
                ngrams[gram] = 1

    return dict(take(k, dict(sorted(ngrams.items(), 
                                    key=lambda x: x[1], 
                                    reverse=True)).items()))

def print_map(map):
    for k,v in map.items():
        print(f"{k}:{v}")


if __name__ == "__main__":
    args = docopt(__doc__)
    k = 10
    n = 4
    text = args['-t']
    if args['-k']:
        k = int(args['-k'])
    if args['-n']:
        n = int(args['-n'])

    print("Words count:")
    print_map(count_words(text))

    num_words_in_sentences = count_words_in_sentence(text)
    print("Average number of words in senteces:")
    print(avg_words_in_sentences(num_words_in_sentences))
    print("Median number of words in sentences:")
    print(median_words_in_sentences(num_words_in_sentences))
    print(f"Top {k} {n}-grams:")
    print_map(top_k_of_top_n(text, k, n))
