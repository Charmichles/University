import os
import numpy as np
from pathlib import Path
import pyttsx3


def get_rhyming_words(list1, list2):
    def is_rhyme(word1, word2):
        return word1[-3:] == word2[-3:]
    
    found_rhyming = False
    word1, rhyming_words = None, None
    while not found_rhyming:
        word1 = list1[np.random.randint(0, len(list1))]
        rhyming_words = [word2 for word2 in list2 if is_rhyme(word1, word2)]
        if len(rhyming_words) != 0:
            found_rhyming = True
    
    return word1, rhyming_words[np.random.randint(0, len(rhyming_words))]


def get_poem_data(dirname):
    words = {}
    filenames = os.listdir(f'{dirname}/words')
    for filename in filenames:
        file = open(f'{dirname}/words/{filename}', 'r')
        words[filename] = [word.replace('\n', '').strip() for word in file.readlines()]
        file.close()

    verse_structures = []
    verse_structures_file = open(f'{dirname}/verse_structures.txt', 'r')
    syntax_map = {}
    for _ in range(len(filenames)):
        word_class, code = verse_structures_file.readline().replace('\n', '').split('-')
        syntax_map[code] = word_class
    while structure := verse_structures_file.readline().replace('\n', ''):
        verse_structures.append(structure)
    verse_structures_file.close()

    poem_structure = []
    poem_structures = ['poem_structure_1.txt', 'poem_structure_2.txt', 'poem_structure_3.txt']
    rand_structure = poem_structures[np.random.randint(0, len(poem_structures))]
    poem_structure_file = open(f'{dirname}/{rand_structure}', 'r')
    stanzas, verses_per_stanza = int(poem_structure_file.readline().split('-')[1]), int(poem_structure_file.readline().split('-')[1])
    rhymes = []
    rhyme_info = poem_structure_file.readline().split('-')[1]
    pairs = rhyme_info.split('|')
    for pair in pairs:
        rhymes.append(tuple(map(int, pair.split(','))))
    for _ in range(stanzas):
        poem_structure.append([])
        for _ in range(verses_per_stanza):
            poem_structure[-1].append(verse_structures[np.random.randint(0, len(verse_structures))])
    poem_structure_file.close()
    
    return words, syntax_map, poem_structure, rhymes


def generate_poem(words, syntax_map, poem_structure, rhymes):
    def conjugate_verb(word, wordtype):
        verb_es_endings = ['s', 'h', 'z', 'y', 'x']
        if wordtype == 'verbs.txt':
            ending = word[-1]
            if ending in verb_es_endings and ending == 'y':
                    word = word[:-1] + 'i'
            word += 's' if ending not in verb_es_endings else 'es'
        return word
    poem = [[[word for word in verse] for verse in stanza] for stanza in poem_structure]
    for stanza in poem:
        for rhyme in rhymes:
            word1_type, word2_type = syntax_map[stanza[rhyme[0]][-1]], syntax_map[stanza[rhyme[1]][-1]]
            stanza[rhyme[0]][-1], stanza[rhyme[1]][-1] = get_rhyming_words(words[word1_type], words[word2_type])
            stanza[rhyme[0]][-1] = conjugate_verb(stanza[rhyme[0]][-1], word1_type)
            stanza[rhyme[1]][-1] = conjugate_verb(stanza[rhyme[1]][-1], word2_type)
        for i in range(len(stanza)):
            for j in range(len(stanza[i])):
                if len(stanza[i][j]) == 1:
                    word_type = syntax_map[stanza[i][j]]
                    words_by_class = words[word_type]
                    stanza[i][j] = words_by_class[np.random.randint(0, len(words_by_class))]
                    stanza[i][j] = conjugate_verb(stanza[i][j], word_type)
          
    return poem


def poem_str(poem):
    poem_fulltxt = ''
    for stanza in poem:
        for i, verse in enumerate(stanza):
            for j, word in enumerate(verse):
                if j == 0:
                    word = word.capitalize()
                sep = ' ' if j != len(verse) - 1 else ''
                poem_fulltxt += word + sep
            sep = ',' if i != len(stanza) - 1 else '.' 
            poem_fulltxt += sep + '\n'
        poem_fulltxt += '\n'
    return poem_fulltxt


def write_poem(filename, poem):
    fout = open(filename, 'w')
    fout.write(poem_str(poem))
    fout.close()


def speak_poem(poem):
    engine = pyttsx3.init()
    engine.setProperty('rate', 140)
    engine.say(poem)
    engine.runAndWait()

if __name__ == '__main__':
    poem_data = get_poem_data('poem_data_1')
    write_poem('poem.txt', generate_poem(*poem_data))